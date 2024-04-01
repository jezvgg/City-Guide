import ruclip
import torch
from PIL import Image
from io import BytesIO
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
        img = Image.open(BytesIO(base64.b64decode(bs4)))
        return img


    def __decode_images(self, images: list):
        start = time.time()
        result = [self.__decode_image(bs4url[2:-1]) for bs4url in images]
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
        # Заменить список на массив из numpy
        with torch.no_grad():
            prompt_latent = self.__predictor.get_text_latents([prompt]).cpu().detach().numpy()[0].reshape(1, -1)
            image_latents = self.__predictor.get_image_latents(images).cpu().detach().numpy()
            result = []
            for latent in image_latents: 
                # Возможно эффективнее будет сразу в косинусуво сходство засунуть 2 списка и взять диагональ
                image_latent = latent.reshape(1, -1)
                result.append(cosine_similarity(prompt_latent, image_latent)[0][0])
        image_index = result.index(max(result))
        print("Find for", time.time()-start)
        return images[image_index], image_index




    @property
    def predictor(self):
        return self.__predictor

    @predictor.setter
    def predictor(self, templates: list):
        self.__predictor = ruclip.Predictor(self.__model, self.__processor, device=self.device, bs=8, templates=templates)