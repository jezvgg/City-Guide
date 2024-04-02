import ruclip
import torch
from PIL import Image
from io import BytesIO
import numpy as np
import base64
import time
from sklearn.metrics.pairwise import cosine_similarity


class CLIP:
    __model = None
    __processor = None
    __predictor = None

    def __init__(self, templates = ['{}', 'это {}', 'на фото {}'], model_name = "ruclip-vit-base-patch32-384"):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.__model, self.__processor = ruclip.load(model_name, device=self.device)
        self.__predictor = ruclip.Predictor(self.__model, self.__processor, device=self.device, bs=8, templates=templates)


    def __decode_image(self, bs4):
        img = Image.open(BytesIO(base64.b64decode(bs4[2:-1])))
        return img


    def __decode_images(self, images: list):
        start = time.time()
        result = [self.__decode_image(bs4url) for bs4url in images]
        print("images decoded for", time.time()-start)
        return result


    def classificate_images(self, images: list, classes: list[str]) -> str:
        images = self.__decode_images(images)

        start = time.time()
        with torch.no_grad():
            text_latents = self.__predictor.get_text_latents(classes)
            pred_labels = self.__predictor.run(images, text_latents)
        print("predicted for", time.time() - start)
        return pred_labels


    def get_by_prompt(self, images: list, prompt: str):
        images = self.__decode_images(images)

        start = time.time()
        with torch.no_grad():
            prompt_latent = self.__predictor.get_text_latents([prompt]).cpu().detach().numpy()
            image_latents = self.__predictor.get_image_latents(images).cpu().detach().numpy()
        print("Vectorized for:", time.time() - start)
        start = time.time()
        result = cosine_similarity(prompt_latent, image_latents)[0]
        print("Cosinus for", time.time() - start)
        index = np.argmax(result)
        return images[index], index


    def get_by_image(self, descriptions: list, user_image: str):
        user_image = self.__decode_image(user_image)

        start = time.time()
        with torch.no_grad():
            user_image_latent = self.__predictor.get_image_latents([user_image]).cpu().detach().numpy()
            latent_descriptions = self.__predictor.get_text_latents(descriptions).cpu().detach().numpy()
        print("Vectorized for:", time.time() - start)
        start = time.time()
        similarity_scores = cosine_similarity(user_image_latent, latent_descriptions)[0]
        print("Cosins in", time.time() - start, "seconds")
        index = np.argmax(similarity_scores)
        return descriptions[index], index


    @property
    def predictor(self):
        return self.__predictor


    @predictor.setter
    def predictor(self, templates: list):
        self.__predictor = ruclip.Predictor(self.__model, self.__processor, device=self.device, bs=8, templates=templates)