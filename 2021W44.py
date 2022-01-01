import pandas as pd

data = pd.read_excel("data/Carl's 2021 cycling.xlsx")
# Convert the Value field to just be Kilometres ridden
# Carl cycles at an average of 30 kilometres per hour whenever he is measuring his sessions in minutes
data.loc[data["Measure"] == "min", "Value"] = (
    data.loc[data["Measure"] == "min", "Value"] * 0.5
)

# Create a field called measure to convert KM measurements into 'Outdoors' and any measurement in 'mins' as 'Turbo Trainer'.
data["measure"] = data["Measure"].apply(
    lambda x: "Outdoors" if x == "km" else "Turbo Trainer"
)

# Count the number of activities per day and work out the total distance cycled Outdoors or on the Turbo Trainer
data["Activites per day"] = data["Type"].groupby(data["Date"]).transform("count")

data = data.pivot_table(
    index=["Date", "Activites per day"], columns="measure", values="Value", aggfunc=sum
).reset_index()

# Ensure there is a row for each date between 1st Jan 2021 and 1st Nov 2021(inclusive)
# This is done after pivot since doing it before may contain to duplicate index values.eg.2021-01-01 has 2 rows.ie multiple activities on same day.
data.index = pd.DatetimeIndex(data["Date"])
data = (
    data.reindex(pd.date_range(data.index.min(), data.index.max()))
    .rename_axis("DtRange")
    .reset_index()
)
data["Date"] = data["DtRange"].dt.date
data.fillna(0, inplace=True)

final = data[["Date", "Activites per day", "Outdoors", "Turbo Trainer"]].copy()
