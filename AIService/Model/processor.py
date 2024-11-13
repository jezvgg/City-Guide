from typing import Protocol, Iterable


class processor(Protocol):
    '''
    Предобработчик данных для моделей на основе архетиктуре CLIP.
    '''

    def encode_text(self, text: str) -> Iterable:
        '''
        Преобразовать текст, для входа в модель.

        Args:
            text (str): текст, который надо преобразовать.

        Returns:
            Iterable: преобразованный текст, который можно передать на вход модели.
        '''
        pass

    def encode_image(self, image) -> Iterable:
        '''
        Преобразовать картинку, для входа в модель.

        Args:
            image (PIL.Image): картинка, который надо преобразовать.

        Returns:
            Iterable: преобразованная картинка, которую можно передать на вход модели.
        '''
        pass