import onnxruntime as ort
import numpy as np

from Src.Model import clip, processor


class ONNX_CLIP(clip):
    '''
    Реализация универсального интерфеса для использования модели CLIP, на основе ONNX.
    '''
    textual: ort.InferenceSession
    visual: ort.InferenceSession
    preprocessor: processor

    def __init__(self, preprocessor: processor, textual_path: str, visual_path: str, provider: str = 'CPUExecutionProvider'):
        '''
        Args:
            preprocessor (processor): класс для предобработки данных для входа в модель.
            textual_path (str): путь до текстовой модели.
            visual_path (str): путь до визуальной модели.
            provider (str): устройство на котором запускать модели.
        '''
        self.preprocessor = preprocessor
        self.textual = self.__load_model(textual_path, [provider])
        self.visual = self.__load_model(visual_path, [provider])


    def __load_model(self, path: str, providers: list[str] = ['CPUExecutionProvider']) -> ort.InferenceSession:
        '''
        Запустить ONNX модель.
        
        Args:
            path (str): путь до ONNX файла модели.
            providers (list[str]): устройства на которых нужно запустить.
        
        Returns:
            onnxruntime.InferenceSession: сессия работы модели.
        '''
        return ort.InferenceSession(path, providers=providers)


    def get_text_latents(self, prompt: str) -> np.ndarray:
        tokens = self.preprocessor.encode_text(prompt)
        inputs = {self.textual.get_inputs()[0].name: tokens}
        output, = self.textual.run(None, inputs)
        return output


    def get_image_latents(self, image) -> np.ndarray:
        tokens = self.preprocessor.encode_image(image)
        inputs = {self.visual.get_inputs()[0].name: tokens}
        output, = self.visual.run(None, inputs)
        return output

        
