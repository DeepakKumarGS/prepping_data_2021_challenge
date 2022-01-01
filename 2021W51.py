# Prepping Data 2021 Week 51

import pandas as pd
import re

data = pd.read_csv("data/PD 2021 Wk 51 Input.csv")

# Split out the store name from the OrderID

data[["StoreName", "OrderID"]] = data["OrderID"].str.split("-", expand=True)

# Turn the Return State field into a binary Returned field
data["Return State"] = data["Return State"].apply(
    lambda x: 1 if x == "Return Processed" else 0
)

# Create a Sales field
data["Unit Price"] = (
    data["Unit Price"].apply(lambda x: re.sub("£", "", x)).astype("float")
)
data["Sales"] = data["Unit Price"] * data["Quantity"]

# Store Dimension Table
store = data.groupby("StoreName", as_index=False)["Order Date"].min()
store["StoreID"] = (
    store[["Order Date", "StoreName"]]
    .apply(tuple, axis=1)
    .rank(method="dense", ascending=True)
    .astype(int)
)
store.sort_values("StoreID", inplace=True)
store.rename(columns={"Order Date": "First Sold", "StoreName": "Store"}, inplace=True)
# Create a dict to map to fact table,
store_map = pd.Series(store["StoreID"].values, index=store["StoreName"]).to_dict()

# Product Dimension Table
product = data.groupby(
    ["Category", "Sub-Category", "Product Name"], as_index=False
).agg({"Order Date": "min", "Unit Price": "min"})
product.rename(columns={"Order Date": "First Sold"}, inplace=True)
product["ProductID"] = (
    product[["First Sold", "Product Name"]]
    .apply(tuple, axis=1)
    .rank(method="dense", ascending=True)
    .astype(int)
)
product.sort_values("ProductID", inplace=True)

product_map = pd.Series(
    product["ProductID"].values, index=product["Product Name"]
).to_dict()

# Customer Dimension Table
customer = data.groupby("Customer", as_index=False).agg(
    {
        "Return State": "sum",
        "OrderID": "nunique",
        "Order Date": "min",
        "Product Name": "count",
    }
)
customer["Return %"] = round(customer["Return State"] / customer["Product Name"], 2)
customer = customer[["Customer", "Return %", "OrderID", "Order Date"]].rename(
    columns={"OrderID": "Number of Orders", "Order Date": "First Order"}
)
customer["CustomerID"] = (
    customer[["First Order", "Customer"]]
    .apply(tuple, axis=1)
    .rank(method="dense", ascending=True)
    .astype(int)
)
customer.sort_values("CustomerID", inplace=True)

customer_map = pd.Series(
    customer["CustomerID"].values, index=customer["Customer"]
).to_dict()

# Map the fact table,
data["Customer"] = data["Customer"].map(customer_map)
data["Product Name"] = data["Product Name"].map(product_map)
data["StoreName"] = data["StoreName"].map(store_map)

data = data[
    [
        "StoreName",
        "Customer",
        "OrderID",
        "Order Date",
        "Product Name",
        "Return State",
        "Quantity",
        "Sales",
    ]
].rename(
    columns={
        "StoreName": "StoreID",
        "Customer": "CustomerID",
        "Product": "ProductID",
        "Return State": "Returned",
    }
)
