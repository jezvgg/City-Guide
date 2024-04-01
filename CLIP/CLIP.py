import ruclip
import torch
from PIL import Image
from io import BytesIO
import base64
import time


class CLIP:
    __model = None
    __processor = None
    __predictor = None

    def __init__(self, templates = ['{}', 'это {}', 'на фото {}'], model_name = "ruclip-vit-base-patch32-384"):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.__model, self.__processor = ruclip.load(model_name, device=self.device)
        self.__predictor = ruclip.Predictor(self.__model, self.__processor, device=self.device, bs=8, templates=templates)


    def __decode_image(self, bs4):
        img = Image.open(BytesIO(base64.b64decode(bs4)))
        return img


    def classificate_images(self, images: list, classes: list[str]) -> str:
        start = time.time()
        images = [self.__decode_image(bs4url[2:-1]) for bs4url in images]
        print(images[0])
        print("images decoded for", time.time()-start)
        start = time.time()
        with torch.no_grad():
            text_latents = self.__predictor.get_text_latents(classes)
            pred_labels = self.__predictor.run(images, text_latents)
        print("predicted for", time.time() - start)
        return pred_labels


    @property
    def predictor(self):
        return self.__predictor

    @predictor.setter
    def predictor(self, templates: list):
        self.__predictor = ruclip.Predictor(self.__model, self.__processor, device=self.device, bs=8, templates=templates)