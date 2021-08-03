from dspipe import Pipe
import pandas as pd
from pathlib import Path
from scipy.stats import entropy


def compute(f0):
    df = pd.read_csv(f0)
    df["name"] = Path(f0).stem
    df = df.rename(columns={"0": "x", "1": "y", "2": "z"})

    df["z"] = df.z == df.z.max()
    # df['z'] = np.exp(df.z)
    # print(df.z)
    # df.loc[df.z<np.percentile(df.z, 95), 'z'] = 0
    # df.loc[df.z<0, 'z'] = 0

    return df


data = Pipe("data/saliancy_map/", input_suffix=".csv", limit=None)(compute, -1)
df = pd.concat(data)

print(df)

info = pd.read_csv("data/us-congress.csv")
info["photo_key"] = info["photo_url"].apply(lambda x: Path(x).stem)
info = info.set_index("photo_key")

# Adjust ethnicity to a binary for analysis
info["ethnicity"] = info["ethnicity"].apply(
    lambda x: "white" if x == "white-american" else "other"
)

df = df.set_index("name")
cols = ["gender", "ethnicity"]
g = pd.DataFrame(df.groupby("name")["z"].apply(entropy).sort_values(ascending=False))

for key in cols:
    df[key] = info[key]
    g[key] = info[key]
df = df.reset_index()

print(g.groupby(cols)["z"].mean())


import pylab as plt

for col, dx in df.groupby(cols):

    grid = dx.groupby(["x", "y"]).mean().reset_index()
    z = grid.values[:, -1]
    z = z.reshape(20, 20).T

    print(col, entropy(z.ravel()))

    plt.figure()
    plt.imshow(z, interpolation=None, vmin=0, vmax=0.11)
    plt.axis("off")
    plt.tight_layout()

    f_save = f"docs/{col[0]}_{col[1]}.jpg"
    plt.savefig(f_save)

# plt.show()
