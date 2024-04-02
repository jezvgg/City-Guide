import unittest
import numpy as np
import pandas as pd
from CLIP.CLIP import CLIP
from sklearn.metrics import accuracy_score
import os

os.environ["TQDM_DISABLE"] = "1"


class test_clip(unittest.TestCase):

    model = CLIP()
    data = pd.read_csv('Tests/photos_v3.csv.xz')

    def test_classificator(self):
        # 20 секунд
        data = self.data.copy()
        classes = list(data['category'].unique())
        data['category'] = data['category'].apply(lambda x: classes.index(x))
        pred = self.model.classificate_images(data['img'], classes)
        data['pred'] = pred
        print("\n\nResult:", accuracy_score(data['category'], data['pred']))

    def test_getting_by_prompt(self):
        # 15 секунд на каждый промпт
        data = self.data.copy()
        prompts = list(data['name'].unique())
        pt = 0
        for prompt in prompts:
            answer = np.where(data['name'] == prompt)[0]
            img, index = self.model.get_by_prompt(data['img'], prompt)
            if index in answer: pt+=1
        print("\n\nResult:", len(prompts)/100 * pt, '%')

    def test_getting_by_image(self):
        data = self.data.copy()
        descriptions = list(data['category'].unique())
        correct_predictions = 0

        for description in descriptions:
            correct_index = np.where(data['category'] == description)[0]
            img, index = self.model.get_by_image(data['img'], [description])

            if index in correct_index:
                correct_predictions += 1

        accuracy = (correct_predictions / len(descriptions)) * 100
        print("\n\nAccuracy:", accuracy, '%')

            