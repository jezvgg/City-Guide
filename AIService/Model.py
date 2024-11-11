import ruclip
import torch
import numpy as np


class CLIP:
    """
    Обёртка для использования модели ИИ.

    Methods:
        !get_text_latents: обязательный метод, векторизует текстовый запрос.
        !get_image_latents: обязательный метод, векторизует картинку.
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
        '''
        Получить векторные представления текстовых запросов.
        
        Args:
            prompts (list[str]): Список текстовых запросов.

        Returns:
            np.ndarray: массив вектороных представлений.
        '''
        latents = self.__predictor.get_text_latents(prompts)

        with torch.no_grad():
            latents = latents.cpu().detach().numpy()

        return latents


    def get_image_latents(self, images: list) -> np.ndarray:
        '''
        Получить векторные представления изображений.
        
        Args:
            prompts (list[str]): Список изображений.

        Returns:
            np.ndarray: массив вектороных представлений.
        '''
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
