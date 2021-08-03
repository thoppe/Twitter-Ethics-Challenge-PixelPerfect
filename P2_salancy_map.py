from twitter_src.crop_api import ImageSaliencyModel
from pathlib import Path
from PIL import Image, ImageDraw
from dspipe import Pipe
import pandas as pd

bin_path = "twitter_src/candidate_crops"
model_path = "twitter_src/fastgaze.vxm"
model = ImageSaliencyModel(
    crop_binary_path=bin_path,
    crop_model_path=model_path,
)


def compute(f0, f1):

    print(f0)
    f_img = Path(f0)

    img = Image.open(f_img)
    w, h = img.size

    output = model.get_output(f_img)

    print(output["salient_point"])

    dx = 5

    for pt in output["all_salient_points"]:
        x, y, z = pt
        draw = ImageDraw.Draw(img)
        z *= dx
        draw.ellipse((x - z, y - z, x + z, y + z), fill="blue", outline="blue")

    x, y = output["salient_point"][0]
    z = 10
    draw.ellipse((x - z, y - z, x + z, y + z), fill="red", outline="black", width=2)

    df = pd.DataFrame(output["all_salient_points"])

    f2 = str(f1).replace(".jpg", ".csv")
    df.to_csv(f2, index=False)

    # draw.rectangle(crop, fill=None, outline='white', width=10)
    # draw.rectangle(crop, fill=None, outline='black', width=2)

    img.save(f1)


P = Pipe("data/raw_photos/", "data/saliancy_map/", output_suffix=".jpg")
P(compute, -1)
