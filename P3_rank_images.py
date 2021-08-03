from twitter_src.crop_api import ImageSaliencyModel
from pathlib import Path
from tqdm import tqdm
import hashlib
from PIL import Image
import numpy as np
from dspipe import Pipe
import tempfile
import json
from wasabi import msg

aspect_ratio = 1.0  # 3 / 2.0
# offset_amounts = range(0, 30, 5)
# offset_amounts = [0, 5, 10, 15, 20, 25]

# 38.6415 pixels across
# offset_amounts = [0, 10, 5, 7, 10, 12]
offset_amounts = [0, 6, 13, 19, 26]

bin_path = "twitter_src/candidate_crops"
model_path = "twitter_src/fastgaze.vxm"
model = ImageSaliencyModel(
    crop_binary_path=bin_path,
    crop_model_path=model_path,
    aspectRatios=[aspect_ratio],
)

save_dest = Path("data/pairwise_cmp")
save_dest.mkdir(parents=True, exist_ok=True)


def evaluate(img0, img1, offset_amount):
    assert img0.size == img1.size
    spacer_img = np.zeros_like(img0)
    offset_img = np.zeros(
        shape=(spacer_img.shape[0], offset_amount, 3), dtype=spacer_img.dtype
    )

    img = np.hstack([offset_img, np.asarray(img0), spacer_img, np.asarray(img1)])

    img = Image.fromarray(img)

    with tempfile.NamedTemporaryFile(suffix=".jpg") as FOUT:
        img.save(FOUT.name)
        output = model.get_output(Path(FOUT.name))

    # df = pd.DataFrame(output["all_salient_points"])
    # print(df)

    # If this is past the mid_width the right image "wins"
    mid_width = img.size[0] // 2
    cond = int(output["salient_point"][0][0] >= mid_width)

    return cond


def compute(pair):

    f0, f1, offset = pair

    if f0 == f1:
        return None

    f0 = Path(f0)
    f1 = Path(f1)

    f_save = Path("data/pairwise_cmp") / f"{f0.stem}-{f1.stem}--{offset:02d}.json"
    if f_save.exists():
        # msg.fail("Skipping", f_save)
        return None

    img0 = Image.open(f0)
    img1 = Image.open(f1)

    info = {"f0": f0.stem, "f1": f1.stem, "side": evaluate(img0, img1, offset)}

    info["offset"] = offset

    key = "".join(sorted(f0.stem + f1.stem)).encode("utf-8")
    hasher = hashlib.sha1()
    hasher.update(key)
    key = hasher.hexdigest()
    info["pair_key"] = key

    key = "".join((f0.stem + f1.stem)).encode("utf-8")
    hasher = hashlib.sha1()
    hasher.update(key)
    key = hasher.hexdigest()
    info["ordered_key"] = key

    # Right side
    if info["side"]:
        info["winner"] = info["f1"]
        info["loser"] = info["f0"]
    # Left side
    else:
        info["winner"] = info["f0"]
        info["loser"] = info["f1"]

    js = json.dumps(info, indent=2)

    with open(f_save, "w") as FOUT:
        FOUT.write(js)

    # msg.good(f_save)


images = list(map(str, Path("data/raw_photos/").glob("*")))

# Take a subset if we don't want to wait
images = images[:]


for f0 in tqdm(images):

    msg.info(f"Starting {f0}")
    pairs = []

    for f1 in images:
        for n in offset_amounts:
            pairs.append([f0, f1, n])

    Pipe(pairs, shuffle=True)(compute, 8)

"""
# Full pairwise combinations, both left AND right
# Grab one more each time so we can view early results
for k in range(50, len(full_images)):
    msg.info(f"Starting k={k}")
    
    images = full_images[:k]    
    pairs = []
    for f0 in tqdm(images):
        for f1 in images:
            for n in offset_amounts:
               pairs.append([f0, f1, n])

    # Shuffle to get some early results
    P = Pipe(pairs, shuffle=False)
    P(compute, 8)
"""
