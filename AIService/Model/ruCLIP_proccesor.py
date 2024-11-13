import json

import numpy as np
import youtokentome as yttm
from PIL import Image

from Model import processor


class ruCLIP_proccesor(processor):
    eos_id = 3
    bos_id = 2
    unk_id = 1
    pad_id = 0

    def __init__(self, config_path: str):
        with open(config_path) as f: config = json.load(f)

        self.mean = config['mean']
        self.std = config['std']
        self.image_resolution = config['image_resolution']
        self.context_lenght = config['context_length']
        self.tokenizer = yttm.BPE(config['BPE_path'])


    def encode_image(self, img) -> np.ndarray:
        if img.mode != 'RGB':
            img = img.convert('RGB')
    
        # Ресайзинг с сохранением аспекта
        img = img.resize((self.image_resolution, self.image_resolution), Image.Resampling.BILINEAR)
        
        # Преобразование изображения в numpy массив
        img_np = np.array(img, dtype=np.float32) / 255.0
        
        # Нормализация
        img_np = (img_np - self.mean) / self.std
        
        # Перемещение канала в начало (для PyTorch формата)
        img_np = np.transpose(img_np, (2, 0, 1))
        
        return img_np.reshape((1, *img_np.shape)).astype(np.float32)


    def encode_text(self, text: str):
        text = text.lower()
        tokens = self.tokenizer.encode([text], output_type=yttm.OutputType.ID, dropout_prob=0.0)[0]
        tokens = tokens[:self.context_lenght-2]
        tokens = [self.bos_id] + tokens + [self.eos_id]
        empty_positions = self.context_lenght - len(tokens)
        if empty_positions > 0:
            tokens = np.hstack((tokens, np.zeros(empty_positions)))  # position tokens after text
        if len(tokens) > self.context_lenght:
            tokens = tokens[:self.context_lenght-1] + tokens[-1:]
        return np.array(tokens, dtype=int).reshape((1, *tokens.shape))