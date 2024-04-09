import ruclip
import torch
from PIL import Image
from io import BytesIO
import numpy as np
import base64
import time
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import faiss


class CLIP:
    __model = None
    __processor = None
    __predictor = None
    text_latents = []
    images_latents = []
    cousine_similitaries = []


    def __init__(self, data_path, templates = ['{}', 'это {}', 'на фото {}'], model_name = "ruclip-vit-base-patch32-384"):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.__model, self.__processor = ruclip.load(model_name, device=self.device)
        self.__predictor = ruclip.Predictor(self.__model, self.__processor, device=self.device, bs=8, templates=templates)

        data = pd.read_csv(data_path)
        images = self.__decode_images(data['img'])
        with torch.no_grad():
            self.images_latents = self.__predictor.get_image_latents(images).cpu().detach().numpy()
            self.text_latents = self.__predictor.get_text_latents(data['name']).cpu().detach().numpy()

        self.latents = np.concatenate((self.images_latents, self.text_latents), axis=1)
        self.dimensions = self.latents[0].size

        self.index = faiss.IndexFlatL2(self.dimensions)
        faiss.normalize_L2(self.latents)
        self.index.add(self.latents)


    def __decode_image(self, bs4):
        img = Image.open(BytesIO(base64.b64decode(bs4[2:-1])))
        return img


    def __decode_images(self, images: list):
        start = time.time()
        result = [self.__decode_image(bs4url) for bs4url in images]
        print("images decoded for", time.time()-start)
        return result


    def get_by_prompt(self, prompt: str):

        start = time.time()
        with torch.no_grad():
            prompt_latent = self.__predictor.get_text_latents([prompt]).cpu().detach().numpy()
        print("Vectorized for:", time.time() - start)
        start = time.time()
        user_latents = np.concatenate((prompt_latent, prompt_latent), axis=1)
        faiss.normalize_L2(user_latents)
        D, I = self.index.search(user_latents, 1)
        print("Cosinus for", time.time() - start)
        return I[0][0]


    def get_by_image(self, user_image: str):
        image = self.__decode_image(user_image)

        start = time.time()
        with torch.no_grad():
            user_image_latent = self.__predictor.get_image_latents([image]).cpu().detach().numpy()
        print("Vectorized for:", time.time() - start)
        start = time.time()
        user_latents = np.concatenate((user_image_latent, user_image_latent), axis=1)
        faiss.normalize_L2(user_latents)
        D, I = self.index.search(user_latents, 1)
        print("Cosins in", time.time() - start, "seconds")
        return I[0][0]


    @property
    def predictor(self):
        return self.__predictor


    @predictor.setter
    def predictor(self, templates: list):
        self.__predictor = ruclip.Predictor(self.__model, self.__processor, device=self.device, bs=8, templates=templates)
