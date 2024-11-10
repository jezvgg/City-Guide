import base64
from io import BytesIO
from PIL import Image
import time

import ruclip
import torch
import numpy as np
from pymilvus import MilvusClient


class CLIP:
    """
    Класс для поиска похожих изображений и текстов с помощью модели CLIP.

    Attributes:
        text_latents (list): Латенты текста.
        images_latents (list): Латенты изображений.
        cousine_similitaries (list): Косинусные похожести.
        index (faiss.Index): Индекс FAISS для поиска похожих латентов.

    Methods:
        get_by_prompt(prompt): Получает индексы похожих латентов по текстовому запросу.
        get_by_image(user_image): Получает индексы похожих латентов по изображению.
        set_index(index_path): Устанавливает индекс FAISS из файла.
        predictor: Свойство для получения или установки предиктора.
    """
    __model = None
    __processor = None
    __predictor = None
    text_latents = []
    images_latents = []
    cousine_similitaries = []
    database: MilvusClient


    def __init__(self, index_path, templates=['{}', 'это {}', 'на фото {}'], model_name="ruclip-vit-base-patch32-384"):
        """
        Инициализирует экземпляр класса CLIP.

        Args:
            index_path (str): Путь до файла с индексом FAISS.
            templates (list): Шаблоны для генерации текстовых латентов.
            model_name (str): Имя модели CLIP.
        """
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.__model, self.__processor = ruclip.load(model_name, device=self.device)
        self.__predictor = ruclip.Predictor(self.__model, self.__processor, device=self.device, bs=8,
                                            templates=templates)
        self.database = MilvusClient(index_path)


    @staticmethod
    def decode_image(bs4):
        """
        Декодирует изображение из base64.

        Args:
            bs4 (str): Строка в кодировке base64.

        Returns:
            PIL.Image: Расшифрованное изображение.
        """
        img = Image.open(BytesIO(base64.b64decode(bs4)))
        return img

    @staticmethod
    def decode_binary(bin):
        """
        Декодирует изображение из бинарного кода.

        Args:
            bin (bytes): Бинарный код изображения.

        Returns:
            PIL.Image: Расшифрованное изображение.
        """
        img = Image.open(BytesIO(bin))
        return img

    @staticmethod
    def decode_images(images: list):
        """
        Декодирует список изображений.

        Args:
            images (list): Список строк в кодировке base64 или бинарных кодов изображений.

        Returns:
            list: Список расшифрованных изображений.
        """
        start = time.time()
        result = [CLIP.decode_image(bs4url) for bs4url in images]
        print("images decoded for", time.time() - start)
        return result

    def get_by_prompt(self, prompt: str, collection_name: str, output_fields: list = '*'):
        """
        Получает индексы похожих латентов по текстовому запросу.

        Args:
            prompt (str): Текстовый запрос.
            collection_name (str): Название коллекции в базе данных.
            output_fields (list): Список возвращаемых полей.

        Returns:
            list: Индексы похожих латентов.
        """
        with torch.no_grad():
            prompt_latent = self.__predictor.get_text_latents([prompt]).cpu().detach().numpy()
        user_latents = np.concatenate((prompt_latent, prompt_latent), axis=1)

        if output_fields == '*': 
            output_fields = [field['name'] for field in self.database.describe_collection(collection_name)['fields'] \
                            if field['type'] < 100 and not field.get('is_primary')]

        res = self.database.search(
            collection_name=collection_name,
            data=user_latents,
            limit=5,
            output_fields = output_fields
        )

        return res

    def get_by_image(self, user_image: Image, collection_name: str, output_fields: list = '*'):
        """
        Получает индексы похожих латентов по изображению.

        Args:
            user_image (PIL.Image): Изображение.
            collection_name (str): Название коллекции в базе данных.
            output_fields (list): Список возвращаемых полей.

        Returns:
            list: Индексы похожих латентов.
        """
        with torch.no_grad():
            user_image_latent = self.__predictor.get_image_latents([user_image]).cpu().detach().numpy()
        user_latents = np.concatenate((user_image_latent, user_image_latent), axis=1)

        if output_fields == '*': 
            output_fields = [field['name'] for field in self.database.describe_collection(collection_name)['fields'] \
                            if field['type'] < 100 and not field.get('is_primary')]
                            # Вынести в отдельную функцию

        res = self.database.search(
            collection_name=collection_name,
            data=user_latents,
            limit=5,
            output_fields=output_fields
        )

        return res


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
