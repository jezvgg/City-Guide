import unittest
import pandas as pd
from time import time
from pathlib import Path
from Model import CLIP
import logging



class test_benchmarks(unittest.TestCase):

    cwf = Path(__file__).resolve().parent
    cwbd = cwf / 'Benchmarks' # Current Working Benhmarks Directory

    # Download data for benchmarks and unzip to ./Tests/Benchmarks
    # https://drive.google.com/file/d/1ae7ehbyXEeCwN5gkfSH6zIAW6V5sCKdV/view?usp=sharing

    prompt_test = [{'benchmark_name':'Иркутск',
                    'index':'irkutsk.index',
                    'prompts': cwbd / 'prompts.csv.xz',
                    'data': cwbd / 'photos_v3.csv.xz'},
                    {'benchmark_name':'Нижний Новгород',
                    'index':'niznii_novgorod.index',
                    'prompts':cwbd / 'prompts_NN.csv.xz',
                    'data':cwbd / 'NN_images_clean.csv.xz'},
                    {'benchmark_name':'Владимир',
                    'index':'vladimir.index',
                    'prompts':cwbd / 'prompt_Vlad.csv.xz',
                    'data':cwbd / 'Vladimir_images_clean.csv.xz'},
                    {'benchmark_name':'Екатеренбург',
                    'index':'ekaterinburg.index',
                    'prompts':cwbd / 'prompts_EKB.csv.xz',
                    'data':cwbd / 'EKB_images_clear.csv.xz'},
                    {'benchmark_name':'Ярославль',
                    'index':'yaroslavl.index',
                    'prompts':cwbd / 'prompts_yrl.csv.xz',
                    'data':cwbd / 'Yaroslavl_images_clean.csv.xz'}]

    images_test = [{'benchmark_name':'Нижний Новгород',
                    'index':'niznii_novgorod.index',
                    'data':cwbd / 'NN_images_clean_test.csv.xz',
                    'test_data': cwbd / 'NN_validate.csv.xz'},
                    {'benchmark_name':'Владимир',
                    'index':'vladimir.index',
                    'data':cwbd / 'Vladimir_images_clean.csv.xz',
                    'test_data': cwbd / 'Vladimir_validate.csv.xz'},
                    {'benchmark_name':'Екатеренбург',
                    'index':'ekaterinburg.index',
                    'data':cwbd / 'EKB_images_clean_test.csv.xz',
                    'test_data': cwbd / 'EKB_validate.csv.xz'},
                    {'benchmark_name':'Ярославль',
                    'index':'yaroslavl.index',
                    'data':cwbd / 'Yaroslavl_images_clean.csv.xz', # некорректный тест
                    'test_data': cwbd / 'Yaroslavl_validate.csv.xz'}]


    def test_getting_by_prompt(self):
        model = CLIP('irkutsk.index')
        times_bench = []
        mean_accuracy = []
        for benhmark in self.prompt_test:
            model.set_index(benhmark['index'])
            prompts = pd.read_csv(benhmark['prompts'])
            data = pd.read_csv(benhmark['data'])

            correct = 0
            times = []
            for prompt, name in zip(prompts['prompts'], prompts['name']):
                start = time()
                indexes = model.get_by_prompt(prompt)

                if data.iloc[indexes[0]]['name'] == name:
                    correct+=1
                times.append(time()-start)
            
            mean_time = sum(times) / len(times)
            times_bench.append(mean_time)
            accuracy = (correct / len(prompts)) * 100
            mean_accuracy.append(accuracy)

            logging.getLogger().info(f"{benhmark['benchmark_name']} {mean_time:.4f} s {accuracy:.2f} %")
        logging.getLogger().info(f"Общий результат {sum(times_bench) / len(times_bench):.4f} s {sum(mean_accuracy)/len(mean_accuracy):.2f} %")


    def test_getting_by_image(self):
        model = CLIP('irkutsk.index')
        times_bench = []
        mean_accuracy = []

        for benhmark in self.images_test:
            print('\n',benhmark['benchmark_name'])
            model.set_index(benhmark['index'])
            data = pd.read_csv(benhmark['data'])
            test_data = pd.read_csv(benhmark['test_data'])

            correct = 0
            times = []
            for image, name in zip(test_data['img'], test_data['name']):
                start = time()
                image = CLIP.decode_image(image)
                indexes = model.get_by_image(image)

                if indexes[0] >= data.shape[0]:
                    print("Error at", indexes[0], data.shape[0])
                    continue

                if data.iloc[indexes[0]]['name'] == name:
                    correct+=1
                times.append(time()-start)

            mean_time = sum(times) / len(times)
            times_bench.append(mean_time)
            accuracy = (correct / len(test_data)) * 100
            mean_accuracy.append(accuracy)

            logging.getLogger().info(f"{benhmark['benchmark_name']} {mean_time:.4f} s {accuracy:.2f} %")
        logging.getLogger().info(f"Общий результат {sum(times_bench) / len(times_bench):.4f} s {sum(mean_accuracy)/len(mean_accuracy):.2f} %")
            