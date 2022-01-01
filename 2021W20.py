### Prepping Data 2021 Week 20

# Input the data file
# Create the mean and standard deviation for each Week
# Create the following calculations for each of 1, 2 and 3 standard deviations:
# The Upper Control Limit (mean+(n*standard deviation))
# The Lower Control Limit (mean-(n*standard deviation))
# Variation (Upper Control Limit - Lower Control Limit)
# Join the original data set back on to these results
# Assess whether each of the complaint values for each Department, Week and Date is within or outside of the control limits
# Output only Outliers
# Produce a separate output worksheet (or csv) for 1, 2 or 3 standard deviations and remove the irrelevant fields for that output.


import pandas as pd
import numpy as np

data = pd.read_csv("data/PD 2021 Wk20 - Complaints per Day.csv")

sd = (
    data.groupby("Week", as_index=False)["Complaints"]
    .agg(["mean", "std"])
    .reset_index()
)

for i in range(1, 4):
    sd[f"Upper Control Limit ({i}SD)"] = sd["mean"] + (i * sd["std"])
    sd[f"Lower Control Limit ({i}SD)"] = sd["mean"] - (i * sd["std"])
    sd[f"Variation ({i}SD)"] = (
        sd[f"Upper Control Limit ({i}SD)"] - sd[f"Lower Control Limit ({i}SD)"]
    )

data = data.merge(sd, how="inner", on="Week")

for i in range(1, 4):
    data[f"Outlier? ({i}SD)"] = np.where(
        (
            (data["Complaints"] > data[f"Upper Control Limit ({i}SD)"])
            | (data["Complaints"] < data[f"Lower Control Limit ({i}SD)"])
        ),
        "Outlier",
        "Not-Outlier",
    )

for i in range(1, 4):
    columns = [
        f"Variation ({i}SD)",
        f"Outlier? ({i}SD)",
        f"Lower Control Limit ({i}SD)",
        f"Upper Control Limit ({i}SD)",
        "std",
        "mean",
        "Date",
        "Week",
        "Complaints",
        "Department",
    ]
    globals()["Outlier_%sSD" % i] = data.loc[
        data[f"Outlier? ({i}SD)"] == "Outlier", columns
    ].rename(
        columns={
            "mean": "Mean",
            "std": "Standard Deviation",
            f"Upper Control Limit ({i}SD)": "Upper Control Limit",
            f"Lower Control Limit ({i}SD)": "Lower Control Limit",
        }
    )


Outlier_1SD.to_csv("output/PD 2021 Wk20 Outliers 1SD.csv", index=False)
Outlier_2SD.to_csv("output/PD 2021 Wk20 Outliers 2SD.csv", index=False)
Outlier_3SD.to_csv("output/PD 2021 Wk20 Outliers 3SD.csv", index=False)
