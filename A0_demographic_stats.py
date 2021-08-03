import pandas as pd

demographic_keys = [
    "gender",
    "ethnicity",
    "religion",
    "openly_lgbtq",
]

df = pd.read_csv("data/us-congress.csv")

for key in demographic_keys:
    g = df.groupby(key).size().sort_values(ascending=False)
    print(key)
    print(g)
