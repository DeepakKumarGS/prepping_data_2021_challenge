# Prepping Data 2021 Week 32

import pandas as pd
import numpy as np

data = pd.read_csv("data/PD 2021 Wk 32 Input - Data.csv")

# Form Flight name

data["Flight Name"] = data["Departure"] + " to " + data["Destination"]

# Workout how many days between the sale and the flight departing

data["days to flight"] = (
    pd.to_datetime(data["Date of Flight"], format="%d/%m/%Y")
    - pd.to_datetime(data["Date"], format="%d/%m/%Y")
).dt.days

# Classify daily sales of a flight as:
# Less than 7 days before departure
# 7 or more days before departure

data["sale of flight"] = np.where(
    data["days to flight"].astype(int) < 7,
    "7 days until the flight",
    "7 days or more until the flight",
)

# Mimic the SUMIFS and AverageIFS functions by aggregating the previous requirements fields by each Flight and Class

avg_sales = (
    data.groupby(["Flight Name", "Class", "sale of flight"], as_index=False)
    .agg({"Ticket Sales": "mean"})
    .round(0)
)

avg_sales = avg_sales.pivot_table(
    values="Ticket Sales",
    index=["Flight Name", "Class"],
    columns="sale of flight",
    aggfunc="sum",
)

avg_sales.reset_index(level=[0, 1], inplace=True)

avg_sales.rename(
    columns={
        "7 days or more until the flight": "Avg. daily sales 7 days or more until the flight",
        "7 days until the flight": "Avg. daily sales less than 7 days until the flight",
    },
    inplace=True,
)

sum_sales = (
    data.groupby(["Flight Name", "Class", "sale of flight"], as_index=False)
    .agg({"Ticket Sales": "sum"})
    .round(0)
)

sum_sales = sum_sales.pivot_table(
    values="Ticket Sales",
    index=["Flight Name", "Class"],
    columns="sale of flight",
    aggfunc="sum",
)

sum_sales.reset_index(level=[0, 1], inplace=True)

sum_sales.rename(
    columns={
        "7 days or more until the flight": "Sales less than 7 days until the flight",
        "7 days until the flight": "Sales 7 days or more until the flight",
    },
    inplace=True,
)

final = pd.merge(avg_sales, sum_sales, how="inner", on=["Flight Name", "Class"])
