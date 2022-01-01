# Prepping Data 2021 Week 39

import pandas as pd
import re

data = pd.read_csv("data/PD 2021 Wk 39 Bike Painting Process - Painting Process.csv")

# Create a Datetime field
# Identify what time each of the different process stage's took place.
# Each process stage is provided with a start time, and there is no overlap between stages. Assume that the final process stage ends when the last update occurs.
data["Datetime"] = pd.to_datetime(
    data["Date"] + " " + data["Time"], format="%d/%m/%Y %H:%M:%S"
)

# Parse the Bike Type and Batch Status for each batch
data["Bike Type"] = data.apply(
    lambda x: x["Data Value"] if x["Data Parameter"] == "Bike Type" else None, axis=1
)
data["Batch Status"] = data.apply(
    lambda x: x["Data Value"] if x["Data Parameter"] == "Batch Status" else None, axis=1
)
data["Name of Process Stage"] = data.apply(
    lambda x: x["Data Value"]
    if x["Data Parameter"] == "Name of Process Stage"
    else None,
    axis=1,
)
# Parse the Actual & Target values for each parameter.
data["Target"] = data.apply(
    lambda x: x["Data Value"] if re.match("^(Target)", x["Data Parameter"]) else None,
    axis=1,
)
data["Actual"] = data.apply(
    lambda x: x["Data Value"] if re.match("^(Actual)", x["Data Parameter"]) else None,
    axis=1,
)

for c in ["Bike Type", "Batch Status", "Name of Process Stage"]:
    data[c] = data.groupby(["Batch No."])[c].ffill()

data = data.loc[
    (data["Data Type"] == "Process Data")
    & (data["Data Parameter"] != "Name of Process Stage"),
]

data["Data Parameter"] = data["Data Parameter"].apply(
    lambda x: re.sub("^(Target|Actual\s)", "", x)
)


data.rename(columns={"Name of Process Stage": "Name of Process Step"}, inplace=True)

data = data[
    [
        "Batch No.",
        "Name of Process Step",
        "Bike Type",
        "Batch Status",
        "Datetime",
        "Data Parameter",
        "Target",
        "Actual",
    ]
]
