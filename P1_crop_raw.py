from twitter_src.crop_api import ImageSaliencyModel
from twitter_src.image_manipulation import process_image, get_image_saliency_map
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps
import numpy as np
from dspipe import Pipe
import tempfile

aspect_ratio = 1.0  # 4 / 2.0

bin_path = "twitter_src/candidate_crops"
model_path = "twitter_src/fastgaze.vxm"
model = ImageSaliencyModel(
    crop_binary_path=bin_path,
    crop_model_path=model_path,
    aspectRatios=[aspect_ratio],
)


def compute(f0, f1):

    print(f0)
    f_img = Path(f0)

    img = Image.open(f_img)
    w, h = img.size

    target_height = 400

    nw = int(w * target_height / h)
    img = img.resize((nw, target_height))

    with tempfile.NamedTemporaryFile(suffix=".jpg") as FOUT:
        img.save(FOUT.name)
        output = model.get_output(Path(FOUT.name))

    # print(output['salient_point'])
    # print(output['crops'])
    # print(output['all_salient_points'])

    crop = output["crops"][0]
    img = img.crop(crop)

    w, h = img.size
    nw = int(w * target_height / h)
    img = img.resize((nw, target_height))

    print(img.size)

    target_width = int(target_height / aspect_ratio)
    img = ImageOps.pad(img, (target_width, target_height))

    img.save(f1)

    # img.show()


P = Pipe(
    "data/raw_photos/", "data/crop_img", output_suffix=".jpg", shuffle=True, limit=None
)
P(compute, -1)
