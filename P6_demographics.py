import pandas as pd
import numpy as np
from scipy.stats import binomtest

df = pd.read_csv("data/offset_ranking_pairwise.csv")
info = pd.read_csv("data/demographic_labels.csv").set_index('filename')
info = info.fillna(0)
print(df.columns)
print(info.columns)

df['is_exploit'] = df['offset_mismatch'] > 0

df = df.set_index('f0')
df["AA_left"] = info["AA"]
df["F_left"] = info["woman"]
df = df.reset_index()

df = df.set_index('f1')
df["AA_right"] = info["AA"]
df["F_right"] = info["woman"]
df = df.reset_index()

cols = ['F_left', 'AA_left']
g = df.groupby(cols)
print(g['is_exploit'].mean())


cols = ['F_right', 'AA_right']
g = df.groupby(cols)
print(g['is_exploit'].mean())


exit()



#print(df[(df.F_left==1) & (df.F_right==1) & (df.AA_left==1) & (df.AA_right==1)]) 

#del df['ordered_key']
del df['offset_mismatch']

cols = ['F_left', 'AA_left', 'F_right', 'AA_right']
g = df.groupby(cols)
print(g['is_exploit'].mean())
print(g['is_exploit'].size())

expected_value = df['is_exploit'].mean()

###########################################################################

key = 'is_exploit'

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

