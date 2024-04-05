import ruclip
import torch
from PIL import Image
from io import BytesIO
import numpy as np
import base64
import time
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances


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
        similarity_scores = cosine_similarity(prompt_latent, self.images_latents)[0] + cosine_similarity(prompt_latent, self.images_latents)[0]
        # result = np.sqrt((self.cousine_similitaries - similarity_scores) ** 2)
        print("Cosinus for", time.time() - start)
        index = np.argmax(similarity_scores)
        return index


    def get_by_image(self, user_image: str):
        image = self.__decode_image(user_image)

        start = time.time()
        with torch.no_grad():
            user_image_latent = self.__predictor.get_image_latents([image]).cpu().detach().numpy()
        print("Vectorized for:", time.time() - start)
        start = time.time()
        similarity_scores = cosine_similarity(user_image_latent, self.images_latents)[0] + cosine_similarity(user_image_latent, self.images_latents)[0]
        # result = np.sqrt((self.cousine_similitaries - similarity_scores) ** 2)
        print("Cosins in", time.time() - start, "seconds")
        index = np.argmax(similarity_scores)
        return index


    @property
    def predictor(self):
        return self.__predictor


    @predictor.setter
    def predictor(self, templates: list):
        self.__predictor = ruclip.Predictor(self.__model, self.__processor, device=self.device, bs=8, templates=templates)
