# Prepping Data Week 35 
# Input the data
# Split up the sizes of the pictures and the frames into lengths and widths
# Remember an inch is 2.54cm
# Frames can always be rotated, so make sure you know which is the min/max side
# See which pictures fit into which frames
# Work out the area of the frame vs the area of the picture and choose the frame with the smallest excess
# Output the data

#Inspiration - Arsene Xie @ArseneXie

import pandas as pd
import re
import numpy as np

data = pd.read_excel("data/PD 2021 Wk 35 Pictures Input.xlsx", sheet_name="Pictures")

frames = pd.read_excel("data/PD 2021 Wk 35 Pictures Input.xlsx", sheet_name="Frames")


def analyse_size(x):
    size_1 = float(re.search("^(\d+)", x).group(1))
    size_2 = float(
        re.search("\D(\d+)\D", x).group(1) if re.search("\D(\d+)\D", x) else size_1
    )
    side_all = (
        [size_1, size_2] if re.search("(cm)", x) else [size_1 * 2.54, size_2 * 2.54]
    )
    side_all.sort()
    return side_all


data["Size Clean"] = data["Size"].apply(lambda x: analyse_size(x))
data["Min Side"] = data["Size Clean"].apply(lambda x: x[0])
data["Max Side"] = data["Size Clean"].apply(lambda x: x[1])

frames.columns = ["Frame"]
frames["Frame Size Clean"] = frames["Frame"].apply(lambda x: analyse_size(x))
frames["Min Side"] = frames["Frame Size Clean"].apply(lambda x: x[0])
frames["Max Side"] = frames["Frame Size Clean"].apply(lambda x: x[1])

frame_fit = pd.merge(data, frames, how="cross")

frame_fit["fit"] = frame_fit.apply(
    lambda x: x["Min Side_y"] >= x["Min Side_x"] and x["Max Side_y"] >= x["Max Side_x"],
    axis=1,
)
frame_fit = frame_fit[frame_fit["fit"]].copy()
frame_fit["Excess Area"] = frame_fit.apply(
    lambda x: np.prod(x["Frame Size Clean"]) - np.prod(x["Size Clean"]), axis=1
)

frame_fit["Min Excess Area"] = (
    frame_fit["Excess Area"].groupby(frame_fit["Picture"]).transform("min")
)

final = frame_fit[frame_fit["Excess Area"] == frame_fit["Min Excess Area"]][
    ["Picture", "Frame", "Max Side_x", "Min Side_x"]
].rename(columns={"Max Side_x": "Max Side", "Min Side_x": "Min Side"})
