import pandas as pd
from dspipe import Pipe
import json


def compute(f0):
    with open(f0) as FIN:
        js = json.load(FIN)
    return js


P = Pipe("data/pairwise_cmp/", shuffle=True)
data = P(compute, -1)
df = pd.DataFrame(data)
df.to_csv("data/ranking_fullset.csv", index=False)
