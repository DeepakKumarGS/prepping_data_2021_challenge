# Prepping Data 2021 W33

import pandas as pd
import xlrd

xls_doc = xlrd.open_workbook("data/PD 2021 Wk33 Allchains Weekly Orders.xlsx")

for index, sheetname in enumerate(xls_doc.sheet_names()):
    globals()["data%s" % index] = pd.read_excel(
        "data/PD 2021 Wk33 Allchains Weekly Orders.xlsx", sheet_name=sheetname
    )
    globals()["data%s" % index]["Reporting Date"] = sheetname

data = pd.concat([data0, data1, data2, data3, data4], axis=0)

data["Reporting Date"] = pd.to_datetime(data["Reporting Date"], format="%Y%m%d")

data.sort_values(["Orders", "Reporting Date"], inplace=True)

data["min reporting date"] = (
    data["Reporting Date"].groupby(data["Orders"]).transform("min")
)
data["max reporting date"] = (
    data["Reporting Date"].groupby(data["Orders"]).transform("max")
)
data["Order Status"] = data.apply(
    lambda x: "New Order"
    if x["Reporting Date"] == x["min reporting date"]
    else "Unfulfilled Order",
    axis=1,
)

# The first time an order appears it should be classified as a 'New Order'
# The week after the last time an order appears in a report (the maximum date) is when the order is classed as 'Fulfilled' 
# Any week between 'New Order' and 'Fulfilled' status is classed as an 'Unfulfilled Order' 
orders = data[data["Reporting Date"] == data["max reporting date"]].copy()
orders["Fulfilled flag"] = orders["max reporting date"] + pd.Timedelta(1, unit="w")
orders = orders[~(orders["Fulfilled flag"] > "2021-01-29")]

orders.loc[:, "Reporting Date"] = orders.loc[:, "Fulfilled flag"]

orders.loc[:, "Order Status"] = "Fulfilled"
#Pull of the data sets together 
#Remove any unnecessary fields
final = pd.concat(
    [
        data[["Order Status", "Orders", "Sale Date", "Reporting Date"]],
        orders[["Order Status", "Orders", "Sale Date", "Reporting Date"]],
    ],
    axis=0,
)

final.sort_values(["Orders", "Reporting Date"], inplace=True)
