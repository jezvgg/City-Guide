import ruclip
import torch
from PIL import Image
from io import BytesIO
import numpy as np
import base64
import pandas as pd
import faiss


def __decode_image(bs4):
    img = Image.open(BytesIO(base64.b64decode(bs4[2:-1])))
    return img


def __decode_images(images: list):
    result = [__decode_image(bs4url) for bs4url in images]
    return result


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
__model, __processor = ruclip.load("ruclip-vit-base-patch32-384", device=device)
__predictor = ruclip.Predictor(__model, __processor, device=device, bs=8, templates=['{}', 'это {}', 'на фото {}'])

data = pd.read_csv('/home/jezvgg/Projects/project/CLIP/Tests/val_img_data.csv')
images = __decode_images(data['img'])
with torch.no_grad():
    images_latents = __predictor.get_image_latents(images).cpu().detach().numpy()
    text_latents = __predictor.get_text_latents(data['name']).cpu().detach().numpy()

latents = np.concatenate((images_latents, text_latents), axis=1)
dimensions = latents[0].size

index = faiss.IndexFlatL2(dimensions)
faiss.normalize_L2(latents)
index.add(latents)

faiss.write_index(index, 'Tests/val.index')