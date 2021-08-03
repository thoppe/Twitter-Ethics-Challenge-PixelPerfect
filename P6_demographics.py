import pandas as pd
from pathlib import Path
from scipy.stats import binomtest

df = pd.read_csv("data/offset_ranking_pairwise.csv")
df["is_exploit"] = df["offset_mismatch"] > 0
df = df.rename(columns={"f0": "left", "f1": "right"})

###############################################################################
# Match demographic data
###############################################################################

info = pd.read_csv("data/us-congress.csv")
info["photo_key"] = info["photo_url"].apply(lambda x: Path(x).stem)
info = info.set_index("photo_key")

demographic_keys = [
    "gender",
    "ethnicity",
]

# Adjust ethnicity to a binary for analysis
info["ethnicity"] = info["ethnicity"].apply(
    lambda x: "white" if x == "white-american" else "other"
)

df = df.rename(columns={"f0": "left", "f1": "right"})

for outer_key in ["left", "right"]:
    df = df.set_index(outer_key)

    for demo_key in demographic_keys:
        key = f"{demo_key}_{outer_key}"
        df[key] = info[demo_key]

    df = df.reset_index()


df["left_key"] = df.ethnicity_left + "_" + df.gender_left
df["right_key"] = df.ethnicity_right + "_" + df.gender_right

# df['left_key'] = df.party_left
# df['right_key'] = df.party_right

# Save personal exploitability
g = df.groupby("left")["is_exploit"].mean().sort_values(ascending=False)
g = pd.DataFrame(g)
g.index.name = "name"
for key in demographic_keys:
    g[key] = info[key]
print(g.groupby(["ethnicity", "gender"])["is_exploit"].mean())

g.to_csv("data/exploitability.csv")

###############################################################################
# Basic table for stats
###############################################################################

stats = pd.DataFrame()

stats["n"] = df.groupby("left_key")["is_exploit"].size()
stats["n"] += df.groupby("right_key")["is_exploit"].size()

stats["k"] = df.groupby("left_key")["is_exploit"].sum()
stats["k"] += df.groupby("right_key")["is_exploit"].sum()

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


#################################################################################
# Interaction table
#################################################################################

df["demographic_key"] = df.apply(
    lambda x: "--".join(sorted([x["left_key"], x["right_key"]])), axis=1
)

stats = pd.DataFrame()

stats["n"] = df.groupby(["left_key", "right_key"])["is_exploit"].size()
stats["k"] = df.groupby(["left_key", "right_key"])["is_exploit"].sum()


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
