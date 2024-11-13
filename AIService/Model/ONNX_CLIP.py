import onnxruntime as ort
import numpy as np

from Model import clip, processor

import logging

class ONNX_CLIP(clip):
    textual: ort.InferenceSession
    visual: ort.InferenceSession
    preprocessor: processor

    def __init__(self, preprocessor: processor, textual_path: str, visual_path: str, provider: str = 'CPUExecutionProvider'):
        self.preprocessor = preprocessor
        self.textual = self.__load_model(textual_path, [provider])
        self.visual = self.__load_model(visual_path, [provider])


    def __load_model(self, path: str, providers: list[str] = ['CPUExecutionProvider']) -> ort.InferenceSession:
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

        
