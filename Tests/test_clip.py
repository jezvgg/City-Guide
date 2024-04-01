import unittest
import pandas as pd
from CLIP.CLIP import CLIP
from sklearn.metrics import accuracy_score


class test_clip(unittest.TestCase):

    model = CLIP()

    def test_classificator(self):
        data = pd.read_csv('Tests/photos_v3.csv.xz')
        classes = list(data['category'].unique())
        data['category'] = data['category'].apply(lambda x: classes.index(x))
        pred = self.model.classificate_images(data['img'], classes)
        data['pred'] = pred
        print("\n\nResult:", accuracy_score(data['category'], data['pred']))