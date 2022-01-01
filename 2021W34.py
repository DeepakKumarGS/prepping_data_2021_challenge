## Prepping Data 2021 W34

# Calculate the Average Monthly Sales for each employee
# In the Targets sheet the Store Name needs cleaning up
# Filter the data so that only employees who are below 90% of their target on average remain
# For these employees, we also want to know the % of months that they met/exceeded their target
# Output the data

import pandas as pd
import numpy as np

data = pd.read_excel("data/2021 Week 34 Input.xlsx", sheet_name="Employee Sales")
target = pd.read_excel("data/2021 Week 34 Input.xlsx", sheet_name="Employee Targets")


data = pd.melt(
    data, id_vars=["Store", "Employee"], value_name="Sales", var_name="Month"
)


# In the Targets sheet the Store Name needs cleaning up

change_dict = {
    "Stratfod": "Stratford",
    "Stratfodd": "Stratford",
    "Statford": "Stratford",
    "Straford": "Stratford",
    "Wimbledan": "Wimbledon",
    "Vimbledon": "Wimbledon",
    "Wimbledone": "Wimbledon",
    "Bristoll": "Bristol",
    "Bristal": "Bristol",
    "Bristole": "Bristol",
    "Yor": "York",
    "Yorkk": "York",
    "Yark": "York",
}

target["Store"] = target["Store"].map(change_dict).fillna(target["Store"])

store = data.merge(target, on=["Store", "Employee"])

store["months target met"] = np.where(store["Sales"] > store["Monthly Target"], 1, 0)

# Calculate the Average Monthly Sales for each employee

store = (
    store.groupby(["Store", "Employee"])
    .agg(
        avg_sales=("Sales", "mean"),
        pct_monthly_target=("months target met", "mean"),
        monthly_target=("Monthly Target", "mean"),
    )
    .reset_index()
)

store = store.loc[store["avg_sales"] < store["monthly_target"] * 0.9]

store["pct_monthly_target"] = np.round(store["pct_monthly_target"] * 100, 0)
store["avg_sales"] = np.round(store["avg_sales"], 0)

col_names = [
    "Store",
    "Employee",
    "Avg monthly Sales",
    "% of months target met",
    "Monthly Target",
]

store.columns = col_names


