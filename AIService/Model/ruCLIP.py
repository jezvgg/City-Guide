import ruclip
import torch
import numpy as np

from Model import clip


class ruCLIP(clip):
    """
    Обёртка для использования модели ruCLIP.

    Methods:
        get_text_latents: векторизует текстовый запрос.
        get_image_latents: векторизует картинку.
    """
    __model = None
    __processor = None
    __predictor = None


    def __init__(self, model_name="ruclip-vit-base-patch32-384", templates=['{}', 'это {}', 'на фото {}']):
        """
        Инициализирует экземпляр класса CLIP.

        Args:
            model_name (str): Имя модели CLIP.
            templates (list): Шаблоны для генерации текстовых латентов.
        """
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.__model, self.__processor = ruclip.load(model_name, device=self.device)
        self.__predictor = ruclip.Predictor(self.__model, self.__processor, device=self.device, bs=8,
                                            templates=templates)


    def get_text_latents(self, prompts: list[str]) -> np.ndarray:
        latents = self.__predictor.get_text_latents(prompts)

        with torch.no_grad():
            latents = latents.cpu().detach().numpy()

        return latents


    def get_image_latents(self, images: list) -> np.ndarray:
        latents = self.__predictor.get_image_latents(images)

        with torch.no_grad():
            latents = latents.cpu().detach().numpy()

        return latents
    

    @property
    def predictor(self):
        """
        Свойство для получения или установки предиктора.

        Returns:
            ruclip.Predictor: Предиктор для модели CLIP.
        """
        return self.__predictor


    @predictor.setter
    def predictor(self, templates: list):
        """
        Устанавливает предиктор для модели CLIP.

        Args:
            templates (list): Шаблоны для генерации текстовых латентов.
        """
        self.__predictor = ruclip.Predictor(self.__model, self.__processor, device=self.device, bs=8,
                                            templates=templates)
