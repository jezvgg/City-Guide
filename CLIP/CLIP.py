import ruclip
import torch
from PIL import Image
from io import BytesIO
import numpy as np
import base64
import time
import faiss


class CLIP:
    __model = None
    __processor = None
    __predictor = None
    text_latents = []
    images_latents = []
    cousine_similitaries = []
    index = None


    def __init__(self, index_path, templates = ['{}', 'это {}', 'на фото {}'], model_name = "ruclip-vit-base-patch32-384"):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.__model, self.__processor = ruclip.load(model_name, device=self.device)
        self.__predictor = ruclip.Predictor(self.__model, self.__processor, device=self.device, bs=8, templates=templates)

        self.set_index(index_path)


    @staticmethod
    def decode_image(bs4):
        img = Image.open(BytesIO(base64.b64decode(bs4[2:-1])))
        return img


    @staticmethod
    def decode_binary(bin):
        img = Image.open(BytesIO(bin))
        return img


    @staticmethod
    def decode_images(images: list):
        start = time.time()
        result = [CLIP.decode_image(bs4url) for bs4url in images]
        print("images decoded for", time.time()-start)
        return result


    def get_by_prompt(self, prompt: str):

        with torch.no_grad():
            prompt_latent = self.__predictor.get_text_latents([prompt]).cpu().detach().numpy()
        user_latents = np.concatenate((prompt_latent, prompt_latent), axis=1)
        faiss.normalize_L2(user_latents)
        D, I = self.index.search(user_latents, 100)
        return I[0]


    def get_by_image(self, user_image: Image):
        
        with torch.no_grad():
            user_image_latent = self.__predictor.get_image_latents([user_image]).cpu().detach().numpy()
        user_latents = np.concatenate((user_image_latent, user_image_latent), axis=1)
        faiss.normalize_L2(user_latents)
        D, I = self.index.search(user_latents, 100)
        return I[0]


    def set_index(self, index_path: str):
        self.index = faiss.read_index(index_path)


    @property
    def predictor(self):
        return self.__predictor


    @predictor.setter
    def predictor(self, templates: list):
        self.__predictor = ruclip.Predictor(self.__model, self.__processor, device=self.device, bs=8, templates=templates)
