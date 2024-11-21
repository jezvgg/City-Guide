from typing import Protocol, Iterable


class clip(Protocol):
    '''
    Абстракный класс обёртки, для использования нейронных сетей с архетиктурой CLIP
    '''

    def get_text_latents(self, prompts: list[str]) -> Iterable:
        '''
        Получить векторные представления текстовых запросов.
        
        Args:
            prompts (list[str]): Список текстовых запросов.

        Returns:
            Iterable: массив вектороных представлений.
        '''
        pass

    def get_image_latents(self, images: list) -> Iterable:
        '''
        Получить векторные представления изображений.
        
        Args:
            prompts (list[Image]): Список изображений.

        Returns:
            np.ndarray: массив вектороных представлений.
        '''
        pass

