import unittest
import numpy as np
import pandas as pd
from CLIP import CLIP
from sklearn.metrics import accuracy_score


class test_clip(unittest.TestCase):

    model = CLIP()
    data = pd.read_csv('Tests/photos_v3.csv.xz')


    def test_getting_by_prompt(self):
        # 15 секунд на каждый промпт
        data = self.data.copy()
        prompts = list(data['name'].unique())
        pt = 0
        for prompt in prompts:
            answer = np.where(data['name'] == prompt)[0]
            index = self.model.get_by_prompt(prompt)
            if index in answer: pt+=1
        print("\n\nResult:", len(prompts)/100 * pt, '%')


    def test_getting_by_image(self):
        data = self.data.copy()
        images = list(data.drop_duplicates(subset=['name'])['img'])
        correct_predictions = 0

        for image in images:
            description = data[data['img'] == image]['name'].iloc[0]
            correct_index = np.where(data['name'] == description)[0]
            index = self.model.get_by_image(image)

            if index in correct_index:
                correct_predictions += 1

        accuracy = (correct_predictions / len(images)) * 100
        print("\n\nAccuracy:", accuracy, '%')

            