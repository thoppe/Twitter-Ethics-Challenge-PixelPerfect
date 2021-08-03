from pathlib import Path
import random
from PIL import Image, ImageDraw
import numpy as np
import pandas as pd
from dspipe import Pipe
import tempfile
import json
from scipy.stats import binomtest


def compute(f0):
    with open(f0) as FIN:
        js = json.load(FIN)
    return js


"""
P = Pipe('data/pairwise_cmp_side/',shuffle=True)
data = P(compute, -1)
df = pd.DataFrame(data)
mu = df.side.mean()

#res = binomtest(df.side.sum(), n=len(df), p=0.5, alternative='two-sided')
#print(res)
#print(f"Analysis of side {mu:0.4} p-value = {res.pvalue:0.8f}")
"""

P = Pipe("data/pairwise_cmp/", shuffle=True)
data = P(compute, -1)
df = pd.DataFrame(data)
df.to_csv("data/ranking_fullset.csv", index=False)

exit()

dx = pd.DataFrame()
dx["win"] = df.groupby("winner").size()
dx["loss"] = df.groupby("loser").size()
dx = dx.fillna(0)
dx["games"] = dx.win + dx.loss
dx["pct"] = dx.win / (dx.games)

dx = dx.sort_values("pct", ascending=False)
dx.index.name = "filename"
dx.to_csv("data/rankings.csv")
print(dx)
