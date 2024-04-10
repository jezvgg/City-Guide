import unittest
import pandas as pd
from CLIP import CLIP
from time import time


class test_clip(unittest.TestCase):


    prompt_test = [{'benchmark_name':'Иркутск',
                    'index':'irkutsk.index',
                    'prompts':'Tests/prompts.csv',
                    'data':'photos_v3.csv.xz'},
                    {'benchmark_name':'Нижний Новгород',
                    'index':'niznii_novgorod.index',
                    'prompts':'Tests/prompts_NN.csv',
                    'data':'NN_images_clean.csv'},
                    {'benchmark_name':'Владимир',
                    'index':'vladimir.index',
                    'prompts':'Tests/prompt_Vlad.csv',
                    'data':'Vladimir_images_clean.csv'},
                    {'benchmark_name':'Екатеренбург',
                    'index':'ekaterinburg.index',
                    'prompts':'Tests/prompts_EKB.csv',
                    'data':'EKB_images_clear (1).csv'},
                    {'benchmark_name':'Ярославль',
                    'index':'yaroslavl.index',
                    'prompts':'Tests/prompts_yrl.csv',
                    'data':'Yaroslavl_images_clean.csv'}]

    images_test = [{'benchmark_name':'Иркутск',
                    'index':'irkutsk.index',
                    'data':'photos_v3.csv.xz',
                    'test_data': 'irk_validate.csv'},
                    {'benchmark_name':'Нижний Новгород',
                    'index':'niznii_novgorod.index',
                    'data':'NN_images_clean_test.csv',
                    'test_data': 'NN_validate.csv'},
                    {'benchmark_name':'Владимир',
                    'index':'vladimir.index',
                    'data':'Vladimir_images_clean.csv',
                    'test_data': 'Vladimir_validate.csv'},
                    {'benchmark_name':'Екатеренбург',
                    'index':'ekaterinburg.index',
                    'data':'EKB_images_clean_test.csv',
                    'test_data': 'EKB_validate.csv'},
                    {'benchmark_name':'Ярославль',
                    'index':'yaroslavl.index',
                    'data':'Yaroslavl_images_clean_test.csv',
                    'test_data': 'Yaroslavl_validate.csv'}]

    def test_getting_by_prompt(self):
        model = CLIP('irkutsk.index')
        for benhmark in self.prompt_test:
            model.set_index(benhmark['index'])
            prompts = pd.read_csv(benhmark['prompts'])
            data = pd.read_csv(benhmark['data'])

            correct = 0
            times = []
            for prompt, name in zip(prompts['prompts'], prompts['name']):
                start = time()
                indexes = model.get_by_prompt(prompt)

                print(data.iloc[indexes[0]]['name'], '|', name, '|', prompt)
                if data.iloc[indexes[0]]['name'] == name:
                    correct+=1
                times.append(time()-start)

            print('\n',benhmark['benchmark_name'])
            print('Mean time:', sum(times) / len(times))
            accuracy = (correct / len(prompts)) * 100
            print("Result:", accuracy, '%')


    def test_getting_by_image(self):
        model = CLIP('irkutsk.index')

        for benhmark in self.image_test:
            model.set_index(benhmark['index'])
            data = pd.read_csv(benhmark['data'])
            test_data = pd.read_csv(benhmark['test_data'])

            correct = 0
            times = []
            for image, name in zip(test_data['img'], test_data['name']):
                start = time()
                indexes = model.get_by_image(image)

                print(data.iloc[indexes[0]]['name'], '|', name, '|', image)
                if data.iloc[indexes[0]]['name'] == name:
                    correct+=1
                times.append(time()-start)

            print('\n',benhmark['benchmark_name'])
            print('Mean time:', sum(times) / len(times))
            accuracy = (correct / len(test_data)) * 100
            print("Result:", accuracy, '%')
