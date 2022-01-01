# Prepping Data 2021 Week 31

import pandas as pd

data = pd.read_csv("data/PD 2021 Wk 31 Input.csv")

# Remove the 'Return to Manufacturer' records

data = data.loc[~(data["Status"] == "Return to Manufacturer")]

# Create a total for each Store of all the items sold

items_sold = data.groupby("Store", as_index=False)["Number of Items"].sum()

items_sold.rename(columns={"Number of Items": "Items sold per store"}, inplace=True)

data = pd.merge(data, items_sold, on="Store", how="inner")
#Aggregate the data to Store sales by Item
final = data[["Store", "Item", "Items sold per store", "Number of Items"]].pivot_table(
    values="Number of Items",
    index=["Store", "Items sold per store"],
    columns="Item",
    aggfunc="sum",
)

final.reset_index(level=[0, 1], inplace=True)
