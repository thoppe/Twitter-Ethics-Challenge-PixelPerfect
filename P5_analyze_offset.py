import pandas as pd
import numpy as np
import seaborn as sns
import pylab as plt
from scipy.stats import binomtest

df = pd.read_csv("data/ranking_fullset.csv")

g = df.groupby("ordered_key")

print(len(df))

df = df.set_index("ordered_key")
idx = g.size() == g.size().max()
print(g.size().max())
df = df.loc[idx]
df = df.reset_index()

print(len(df))

x = g["side"].mean()
invalid = len(x) - ((x == 0) | (x == 1)).sum()
print(f"Fraction invalid {invalid/len(x):0.3f}")

g = df.groupby(["f0", "f1"])
#gx = g["side"].mean().apply(lambda x: (1 - np.abs(2 * x - 1))).reset_index()
gx = g["side"].mean().apply(lambda x: (1 - np.abs(2 * x - 1)) > 0).reset_index()


gx = gx.rename(columns={"side":"offset_mismatch"})
gx.to_csv("data/offset_ranking_pairwise.csv", index=False)
print(gx)
exit()

sns.displot(gx, binrange=(0, 1))

print("Fraction swapped across pairwise offsets")
print(gx)

print("Fraction swapped across all offsets")
gz = gx.groupby("f0").mean()
print(gz)

print(f"Fraction of people invalid to somebody {float((gz>0).mean()):0.3f}")

plt.figure()
sns.histplot(gx.groupby("f0").mean(), binrange=(0, 1))

plt.show()


# import seaborn as sns
# import pylab as plt

# plt.show()

"""
for key, dx in df.groupby('ordered_key'):
    #if len(dx) < 60:
    #    continue
    dx = dx.sort_values('offset')
    print(dx[['offset','side']])
    print(dx.side.mean())
    plt.plot(dx.offset, dx.side)

plt.show()
"""
