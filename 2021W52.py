# Prepping Data 2021 Week 52

import pandas as pd

compliants = pd.read_excel("data/PD 2021 Wk 52 Input.xlsx", sheet_name="Complaints")
dept = pd.read_excel(
    "data/PD 2021 Wk 52 Input.xlsx", sheet_name="Department Responsbile"
)

# Count the number of complaints per customer
compliants["Compliants per Person"] = compliants.groupby("Name", as_index=False)[
    "Complaint"
].transform("nunique")
compliants.sort_values(["Compliants per Person"], inplace=True)
# Join the 'Department Responsible' data set to allocate the complaints to the correct department
dept["Keyword"] = dept["Keyword"].str.lower()
dept_map = pd.Series(dept["Department"].values, index=dept["Keyword"]).to_dict()

# For any complaint that isn't classified, class the department as 'unknown' and the complaint cause as 'other'
compliants["Compliants causes"] = [
    [a for a, b in dept_map.items() if a in c] for c in compliants["Complaint"]
] # Uses list comprehension

compliants = compliants.explode("Compliants causes")
compliants["Compliants causes"].fillna("other", inplace=True)

# Create a comma-separated field for all the keywords found in the complaint for each department
final = compliants.merge(
    dept, how="left", left_on="Compliants causes", right_on="Keyword"
)
final.loc[final["Compliants causes"] == "other", "Department"] = "Unknown"

final["Compliants causes"] = final.groupby(
    ["Name", "Complaint", "Department", "Compliants per Person"], as_index=False
)["Compliants causes"].transform(lambda x: ", ".join(x))

final.drop("Keyword", axis=1, inplace=True)
final.drop_duplicates(inplace=True)
