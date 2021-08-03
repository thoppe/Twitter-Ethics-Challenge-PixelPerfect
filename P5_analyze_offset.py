import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import binomtest

# nrows = 2000
nrows = None
df = pd.read_csv("data/ranking_fullset.csv", nrows=nrows)
g = df.groupby("ordered_key")

"""
# Remove incomplete computations (not needed once P3_rank_images.py is done!)
df = df.set_index("ordered_key")
idx = g.size() == g.size().max()
print(g.size().max())
df = df.loc[idx]
df = df.reset_index()
"""

###############################################################################
# Save offsets to disk
###############################################################################

x = g["side"].mean()
invalid = len(x) - ((x == 0) | (x == 1)).sum()
print(f"Fraction invalid {invalid/len(x):0.3f}")

g = df.groupby(["f0", "f1"])
gx = pd.DataFrame(g["side"].mean())
gx["offset_mismatch"] = g["side"].mean().apply(lambda x: (1 - np.abs(2 * x - 1)))
gx = gx.reset_index()

gx.to_csv("data/offset_ranking_pairwise.csv", index=False)

###############################################################################
# Match demographic data
###############################################################################

info = pd.read_csv("data/us-congress.csv")
info["photo_key"] = info["photo_url"].apply(lambda x: Path(x).stem)
info = info.set_index("photo_key")


demographic_keys = [
    "gender",
    "ethnicity",
    "party",
]

# Adjust ethnicity to a binary for analysis
info["ethnicity"] = info["ethnicity"].apply(
    lambda x: "white" if x == "white-american" else "other"
)

df = df.rename(columns={"f0": "left", "f1": "right"})

for outer_key in ["left", "right", "winner"]:
    df = df.set_index(outer_key)

    for demo_key in demographic_keys:
        key = f"{demo_key}_{outer_key}"
        df[key] = info[demo_key]

    df = df.reset_index()

df["left_key"] = df.ethnicity_left + "_" + df.gender_left
df["right_key"] = df.ethnicity_right + "_" + df.gender_right

# df["left_key"] = df.party_left
# df["right_key"] = df.party_right

df["left_winner"] = df["side"] == 0
df["right_winner"] = df["side"] == 1


###############################################################################
# Basic table for stats
###############################################################################

stats = pd.DataFrame()

stats["n"] = df.groupby("left_key")["left_winner"].size()
stats["n"] += df.groupby("right_key")["right_winner"].size()

stats["k"] = df.groupby("left_key")["left_winner"].sum()
stats["k"] += df.groupby("right_key")["right_winner"].sum()

stats["pct"] = stats.k / stats.n
expected_value = stats.k.sum() / stats.n.sum()
stats.index.name = "key"

stats["pvalue"] = [
    binomtest(int(row["k"]), int(row["n"]), p=expected_value).pvalue
    for _, row in stats.iterrows()
]

print(stats.reset_index().sort_values("pct", ascending=True).reset_index(drop=True))
print()

#################################################################################
# Interaction table
#################################################################################

df["demographic_key"] = df.apply(
    lambda x: "--".join(sorted([x["left_key"], x["right_key"]])), axis=1
)

stats = pd.DataFrame()

stats["n"] = df.groupby(["left_key", "right_key"])["left_winner"].size()
stats["k"] = df.groupby(["left_key", "right_key"])["left_winner"].sum()


stats["pct"] = stats.k / stats.n
expected_value = stats.k.sum() / stats.n.sum()
stats.index.name = "key"

stats["pvalue"] = [
    binomtest(int(row["k"]), int(row["n"]), p=expected_value).pvalue
    for _, row in stats.iterrows()
]
stats["sig"] = stats.pvalue < 0.01
print(stats.reset_index().sort_values("pct", ascending=True).reset_index(drop=True))
print()
