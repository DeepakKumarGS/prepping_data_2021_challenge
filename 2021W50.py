# Prepping Data 2021 Week 50

import pandas as pd

oct = pd.read_excel("data/PD 2021 Wk 50 Input.xlsx", sheet_name="October")
nov = pd.read_excel("data/PD 2021 Wk 50 Input.xlsx", sheet_name="November")


oct.rename(columns={"Unnamed: 7": "Oct YTD Total"}, inplace=True)
# Fill in the Salesperson names for each row (the name appears at the bottom of each monthly grouping)
oct["Oct YTD Total"] = oct["Oct YTD Total"].fillna(method="bfill")
oct["Salesperson"] = oct["Salesperson"].fillna(method="bfill")
oct = oct[pd.notna(oct["Date"])]
oct["Month"] = "October"

nov["Salesperson"] = nov["Salesperson"].fillna(method="bfill")
nov = nov[pd.notna(nov["Date"])]

nov["Month Total"] = nov.groupby(["Salesperson"])["Total"].transform("sum")

nov["Month"] = "November"

data = pd.concat([oct, nov])
# Bring out the YTD information from the October tracker and use it to create YTD totals for November too
data["Oct YTD Total"] = data.groupby(["Salesperson"])["Oct YTD Total"].transform("max")

data["YTD Total"] = data.apply(
    lambda x: x["Oct YTD Total"]
    + (x["Month Total"] if x["Month"] == "November" else 0),
    axis=1,
)


# Reshape the data so all the bike types are in a single column
final = pd.melt(
    data.drop(["RowID", "Oct YTD Total", "Month", "Month Total", "Total"], axis=1),
    id_vars=["Date", "Salesperson", "YTD Total"],
    value_name="Sales",
    var_name="Bike Type",
)
