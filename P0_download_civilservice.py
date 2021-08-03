import pandas as pd
import requests
from dspipe import Pipe
from wasabi import msg

senate = pd.read_csv("data/us-senate.csv")
house = pd.read_csv("data/us-house.csv")
congress = pd.concat([senate, house])
congress.to_csv("data/us-congress.csv")

df = congress
photos = df.photo_url


def download(url, f1):

    r = requests.get(url)
    assert r.ok

    with open(f1, "wb") as FOUT:
        FOUT.write(r.content)

    msg.good(f1)


Pipe(photos, "data/raw_photos", output_suffix=".jpg")(download, 1)
