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
    "party",
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

print(g)
exit()
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

print(stats.reset_index().sort_values("pct", ascending=True))
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
print(stats.reset_index().sort_values("pct", ascending=True))
print()


###############################################################################################

exit()


# Map a few of the demographic keys to binary

# df['female'] = info['gender'] == 'female'
# df['white'] = info['ethnicity'] == 'white-american'
# df['AA'] = info['ethnicity'] == 'african-american'

# df['white'] = df['ethnicity'] == 'white-american'
# info['white'] = info['ethnicity'] == 'white-american'

info["AA"] = info["ethnicity"] == "african-american"
info["ethnicity"] = info["ethnicity"].apply(
    lambda x: "white" if x == "white-american" else "other"
)

demographic_keys = [
    "gender",
    "ethnicity",
    #'white',
    #'ethnicity',
    #'religion',
    #'openly_lgbtq',
]

for outer_key in ["left", "right"]:
    df = df.set_index(outer_key)

    for demo_key in demographic_keys:
        key = f"{demo_key}_{outer_key}"
        df[key] = info[demo_key]

    df = df.reset_index()

cols = ["gender_left", "gender_right"]
g = df.groupby(cols)
print(df.is_exploit.mean())
print(g.size())
print(g["is_exploit"].mean().reset_index())

cols = ["gender_left", "ethnicity_left", "gender_right", "ethnicity_right"]
g = df.groupby(cols)
print(df.is_exploit.mean())
print(g.size())
dx = g["is_exploit"].mean().reset_index()
print(dx)


exit()

g = df.groupby(cols)
print(g["is_exploit"].mean())


cols = ["F_right", "AA_right"]
g = df.groupby(cols)
print(g["is_exploit"].mean())


exit()


# print(df[(df.F_left==1) & (df.F_right==1) & (df.AA_left==1) & (df.AA_right==1)])

# del df['ordered_key']
del df["offset_mismatch"]

cols = ["F_left", "AA_left", "F_right", "AA_right"]
g = df.groupby(cols)
print(g["is_exploit"].mean())
print(g["is_exploit"].size())

expected_value = df["is_exploit"].mean()

###########################################################################

key = "is_exploit"

stats = pd.DataFrame()
stats["n"] = g[key].size()
stats["k"] = g[key].sum()

pv = []


for idx, row in stats.iterrows():
    p = binomtest(row["k"], row["n"], p=expected_value).pvalue
    pv.append(p)

stats["p"] = pv
stats[key] = g[key].mean()
print(stats)
print("*********************************************************************")
stats = stats[stats.p < 0.05]
print(stats)
