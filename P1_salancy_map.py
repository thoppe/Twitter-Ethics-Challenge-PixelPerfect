# from twitter_src.crop_api import ImageSaliencyModel
# from twitter_src.image_manipulation import process_image, get_image_saliency_map
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps
import numpy as np
from dspipe import Pipe

import torch
from SAL_CODE.src.model import SODModel
from SAL_CODE.src.dataloader import InfDataloader, SODLoader

# https://github.com/sairajk/PyTorch-Pyramid-Feature-Attention-Network-for-Saliency-Detection
f_model = "best-model_epoch-204_mae-0.0505_loss-0.1370.pth"

device = "cuda"
model = SODModel()
chkpt = torch.load(args.model_path, map_location=device)
model.load_state_dict(chkpt["model"])
model.to(device)
model.eval()

exit()


def compute(f0, f1):

    print(f0)
    f_img = Path(f0)

    img = Image.open(f_img)
    w, h = img.size
    exit()

    target_height = 600

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
    "data/crop_img", "data/saliancy_map", output_suffix=".npy", shuffle=True, limit=None
)
P(compute, 1)
