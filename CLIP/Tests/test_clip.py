import unittest
import pandas as pd
from CLIP import CLIP


class test_clip(unittest.TestCase):


    def test_getting_by_prompt(self):
        model = CLIP('irkutsk.index')

        # 0.011 секунд на каждый промпт
        # 98%
        prompts = pd.read_csv('Tests/prompts.csv')
        data = pd.read_csv('photos_v3.csv.xz')
        correct = 0
        for prompt, name in zip(prompts['prompts'], prompts['name']):
            index = model.get_by_prompt(prompt)

            if data.iloc[index]['name'] == name: 
                correct+=1

        accuracy = (correct / len(prompts)) * 100
        print("\n\nResult:", accuracy, '%')


    def test_getting_by_image(self):
        model = CLIP('Tests/val.index')

        # 70%

        data = pd.read_csv('Tests/val_img_data.csv')
        images = pd.read_csv('Tests/test_img_data.csv')

        correct_predictions = 0

        for image, name in zip(images['img'], images['name']):

            index = model.get_by_image(image)

            if data.iloc[index]['name'] == name:
                correct_predictions += 1

        accuracy = (correct_predictions / len(images)) * 100
        print("\n\nAccuracy:", accuracy, '%')

            