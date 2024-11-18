import base64
from io import BytesIO
from PIL import Image

import numpy as np
from pymilvus import MilvusClient

from Model import clip


class service:
    """
    Сервис реализующий логику работы с базой данных и моделью ИИ.

    Attributes:
        databse: MilvusClient - объект векторной базы данных
        model: CLIP - модель ИИ, которая используется в поиске
    """
    model: clip
    database: MilvusClient


    def __init__(self, database: MilvusClient, model: clip):
        """
        Инициализирует сервис получения картинок по запросу

        Args:
            databse: MilvusClient - объект векторной базы данных
            model: CLIP - модель ИИ, которая используется в поиске
        """
        self.model = model
        self.database = database


    def __get_by_latents(self, user_latents: np.ndarray, collection_name: str, limit: int = 5, output_fields: list = '*'):
        '''
        Получает данные по вектору.

        Args:
            user_latents (Iterable): вектор признаков по которому делать поиск.

        Returns:
             list[list[dict[str:obj]]]: Результат поиска в базе данных.
        '''
        if output_fields == '*': output_fields = self.get_all_fields(collection_name)

        res = self.database.search(
            collection_name=collection_name,
            data=user_latents,
            limit=limit,
            output_fields = output_fields
        )

        return res


    def get_by_prompt(self, prompt: str, collection_name: str, limit: int = 5, output_fields: list = '*'):
        """
        Ищет наиболее похожие места по текстовому запросу.

        Args:
            prompt (str): Текстовый запрос.
            collection_name (str): Название коллекции в базе данных.
            limit (int): Количество возвращаемых записей.
            output_fields (list): Список возвращаемых полей. * - значит, что все.

        Returns:
            list[list[dict[str:obj]]]: Результат поиска в базе данных.
        """
        prompt_latent = self.model.get_text_latents(prompt)
        user_latents = np.concatenate((prompt_latent, prompt_latent), axis=1)

        return self.__get_by_latents(user_latents, collection_name, limit, output_fields)


    def get_by_image(self, user_image: Image, collection_name: str, limit: int = 5, output_fields: list = '*'):
        """
        Ищет наиболее похожие места по изображению

        Args:
            user_image (PIL.Image): Картинка.
            collection_name (str): Название коллекции в базе данных.
            limit (int): Количество возвращаемых записей.
            output_fields (list): Список возвращаемых полей. * - значит, что все.

        Returns:
            list[list[dict[str:obj]]]: Результат поиска в базе данных.
        """
        image_latent = self.model.get_image_latents(user_image)
        user_latents = np.concatenate((image_latent, image_latent), axis=1)

        return self.__get_by_latents(user_latents, collection_name, limit, output_fields)


    def get_by_query(self, prompt: str, user_image: Image, \
        collection_name: str, limit: int = 5, output_fields: list = '*'):
        '''
        Ищет наиболее похожие места по изображению и текстовому запросу.

        Args:
            prompt (str): Текстовый запрос.
            user_image (PIL.Image): Картинка.
            collection_name (str): Название коллекции в базе данных.
            limit (int): Количество возвращаемых записей.
            output_fields (list): Список возвращаемых полей. * - значит, что все.

        Returns:
            list[list[dict[str:obj]]]: Результат поиска в базе данных.
        '''
        image_latent = self.model.get_image_latents(user_image)
        prompt_latent = self.model.get_text_latents(prompt)
        user_latents = np.concatenate((image_latent, prompt_latent), axis=1)

        return self.__get_by_latents(user_latents, collection_name, limit, output_fields)


    def get_all_fields(self, collection_name: str):
        '''
        Возвращает все поля коллекции, кроме id и векторов.

        Args:
            collection_name (str): название коллекции в базе данных.

        Returns:
            list: Список полей в колекции.
        '''
        return [field['name'] for field in self.database.describe_collection(collection_name)['fields'] \
                            if field['type'] < 100 and not field.get('is_primary')]


    @staticmethod
    def create_reponse(obj: list[list[dict]]):
        '''
        Конвертировать результат поиска в базе данных в JSON-like объект для отправки.
        '''
        indexes = set([])
        response = []
        for item in obj[0]: 
            # 0 элемент берём, потому что не используем под группы в milvus
            if item['entity']['name'] in indexes: continue
            indexes.add(item['entity']['name'])
            response.append({'id':item['id']} | item['entity'])
        return response


    @staticmethod
    def decode_image(bs4):
        """
        Декодирует изображение из base64.

        Args:
            bs4 (str): Строка в кодировке base64.

        Returns:
            PIL.Image: Расшифрованное изображение.
        """
        return service.decode_binary(base64.b64decode(bs4))


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
        result = [service.decode_image(bs4url) for bs4url in images]
        return result
