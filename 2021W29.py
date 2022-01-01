## Prepping Data 2021 Week 29 

import pandas as pd
import re

event = pd.read_excel(
    "data/PD 2021 Wk29 Olympic Events.xlsx", sheet_name="Olympics Events"
)
venue = pd.read_excel("data/PD 2021 Wk29 Olympic Events.xlsx", sheet_name="Venues")


# Create a correctly formatted DateTime field

event["day"] = event["Date"].apply(lambda x: re.search("(\d+)", x).group(1))
event["month"] = event["Date"].apply(lambda x: re.search("_(\w+)_", x).group(1))
event["year"] = event["Date"].apply(lambda x: re.search("_(\d+)", x).group(1))


event["Date_Format"] = event["day"] + " " + event["month"] + " " + event["year"]

event["UK Date Time"] = event.apply(
    lambda x: x["Date_Format"] + " " + ("0:00" if x["Time"] == "xx" else x["Time"]),
    axis=1,
)

event["UK Date Time"] = event["UK Date Time"].apply(
    lambda x: pd.to_datetime(x, format="%d %B %Y %H:%M")
)

# Parse the event list so each event is on a separate row

clean_sport = {
    "Softball/Baseball": "Baseball/Softball",
    "Softball": "Baseball/Softball",
    "Artistic Gymnastic": "Artistic Gymnastics",
    "Baseball": "Baseball/Softball",
    "Rugby.": "Rugby",
    "Beach Volley": "Beach Volleyball",
    "Wrestling.": "Wrestling",
    "Skateboarding.": "Skateboarding",
    "Boxing.": "Boxing",
    "Beach Volleybal": "Beach Volleyball",
}

## Replace few sports with those matching with venue df.

event["Sport"] = event["Sport"].map(clean_sport).fillna(event["Sport"])
## Removing whitespace from the sports column in venue df:
venue["Sport"] = venue["Sport"].str.strip()
venue["Venue"] = venue["Venue"].str.title()

# pd.DataFrame([map(str.strip,x) for x in event['Events'].str.split(',').values.tolist()])

event = pd.concat(
    [
        event[["Date", "UK Date Time", "Sport", "Venue"]],
        pd.DataFrame(
            [map(str.strip, x) for x in event["Events"].str.split(",").values.tolist()]
        ),
    ],
    axis=1,
    sort=False,
)

event = (
    event.melt(
        id_vars=[e for e in event.columns if not re.match("^\d", str(e))],
        value_name="Event",
        var_name="ToDrop",
    )
    .drop("ToDrop", axis=1)
    .dropna(subset=["Event"])
    .reset_index(drop=True)
)

event["Medal Ceremony?"] = event["Event"].apply(
    lambda x: bool(re.search("Victory Ceremony", x)) or bool(re.search("Gold Medal", x))
)

venue[["Latitude", "Longitude"]] = venue["Location"].str.split(",", expand=True)

venue = venue[["Latitude", "Longitude", "Venue", "Sport"]].drop_duplicates()

event["Venue"] = event["Venue"].str.title()
event["Sport"] = event["Sport"].str.title()

## Due to change in titlecase, there are few formatting changes for below sports. Reformatting those,
change_sport = {
    "3X3 Basketball": "3x3 Basketball",
    "Cycling Bmx Racing": "Cycling BMX Racing",
    "Cycling Bmx Freestyle": "Cycling BMX Freestyle",
}

event["Sport"] = event["Sport"].map(change_sport).fillna(event["Sport"])

sports_group = {
    "Opening Ceremony": "Ceremony",
    "Closing Ceremony": "Ceremony",
    "Table Tennis": "Tennis",
    "Judo": "Martial Arts",
    "Karate": "Martial Arts",
    "Artistic Gymnastics": "Gymnastics",
    "Trampoline Gymnastics": "Gymnastics",
    "Cycling BMX Freestyle": "Cycling",
    "Cycling BMX Racing": "Cycling",
    "Marathon Swimming": "Swimming",
    "Beach Volleyball": "Volleyball",
    "3x3 Basketball": "Basketball",
    "Canoe Sprint": "Canoeing",
    "Canoe Slalom": "Canoeing",
    "Artistic Swimming": "Swimming",
    "Taekwondo": "Martial Arts",
    "Cycling Track": "Cycling",
    "Cycling Mountain Bike": "Cycling",
    "Cycling Road": "Cycling",
    "Baseball/Softball": "Baseball",
}

final = pd.merge(
    event,
    venue[["Latitude", "Longitude", "Sport", "Venue"]],
    on=["Sport", "Venue"],
    how="left",
)

final["Sports Group"] = final["Sport"].map(sports_group).fillna(final["Sport"])
