import pandas as pd
import numpy as np
from functools import reduce

other_airline = pd.read_excel(
    "data/PD 2021 Wk 23 NPS Input.xlsx", sheet_name="Airlines"
)
prep_airlines = pd.read_excel(
    "data/PD 2021 Wk 23 NPS Input.xlsx", sheet_name="Prep Air"
)
# Combine Prep Air dataset with other airlines
air_data = pd.concat([other_airline, prep_airlines], axis=0)
# Exclude any airlines who have had less than 50 customers respond
air_data["Total_Customers"] = air_data.groupby("Airline")["CustomerID"].transform(
    "nunique"
)
air_data = air_data.loc[
    air_data["Total_Customers"] >= 50,
]
# Classify customer responses to the question in the following way:
# 0-6 = Detractors
# 7-8 = Passive
# 9-10 = Promoters
air_data["customer_response"] = np.where(
    (
        (air_data["How likely are you to recommend this airline?"] >= 0)
        & (air_data["How likely are you to recommend this airline?"] <= 6)
    ),
    "Detractors",
    np.where(
        (
            (air_data["How likely are you to recommend this airline?"] >= 7)
            & (air_data["How likely are you to recommend this airline?"] <= 8)
        ),
        "Passive",
        "Promoters"
    )
)

# Calculate the NPS for each airline
# NPS = % Promoters - % Detractors
num_promoters = (
    air_data.loc[
        air_data["customer_response"] == "Promoters",
    ]
    .groupby("Airline")["customer_response"]
    .count()
    .reset_index()
    .rename(columns={"customer_response": "# of promoters"})
)
num_detractors = (
    air_data.loc[
        air_data["customer_response"] == "Detractors",
    ]
    .groupby("Airline")["customer_response"]
    .count()
    .reset_index()
    .rename(columns={"customer_response": "# of detractors"})
)
num_customers = (
    air_data["Airline"]
    .value_counts()
    .reset_index()
    .rename(columns={"Airline": "# customers", "index": "Airline"})
)
dfs = [num_customers, num_detractors, num_promoters]
final = reduce(
    lambda left, right: pd.merge(left, right, on="Airline", how="inner"), dfs
)
final["% promoters"] = np.floor((final["# of promoters"] / final["# customers"]) * 100)
final["% detractors"] = np.floor(
    (final["# of detractors"] / final["# customers"]) * 100
)
final["NPS"] = final["% promoters"] - final["% detractors"].astype(int)

# Calculate the average and standard deviation of the dataset
final["average"] = final["NPS"].mean()
final["std"] = final["NPS"].std()

# Take each airline's NPS and subtract the average, then divide this by the standard deviation
final["Z Score"] = np.round((final["NPS"] - final["average"]) / final["std"], 2)

# Filter to just show Prep Air's NPS along with their Z-Score
prep_air_score = final.loc[
    final["Airline"] == "Prep Air", ["Airline", "NPS", "Z Score"]
]

prep_air_score.to_csv('output/PD 2021 W23 Output.csv',index=False)