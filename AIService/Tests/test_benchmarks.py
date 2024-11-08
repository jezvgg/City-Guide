import unittest
from time import time
from pathlib import Path
import logging
import json

import pandas as pd

from Model import CLIP



class test_benchmarks(unittest.TestCase):

    cwf = Path(__file__).resolve().parent
    cwbd = cwf / 'Benchmarks' # Current Working Benhmarks Directory

    # Old data
    # https://drive.google.com/file/d/1ae7ehbyXEeCwN5gkfSH6zIAW6V5sCKdV/view?usp=sharing
    # New data
    # https://drive.google.com/file/d/1wSJKfq1msri_w0op2VE9shsaNhxPdW2U/view?usp=sharing


    with open(cwbd / 'text' / 'config.json') as f: prompt_test = json.load(f)
    with open(cwbd / 'image' / 'config.json') as f: images_test = json.load(f)


    def test_getting_by_prompt(self):
        model = CLIP('irkutsk.index')
        times_bench = []
        mean_accuracy = []
        for benhmark in self.prompt_test:
            model.set_index(benhmark['index'])
            prompts = pd.read_csv(self.cwbd / 'text' / benhmark['prompts'])
            data = pd.read_csv(self.cwbd / 'text' / benhmark['data'])

            correct = 0
            times = []
            for prompt, name in zip(prompts['prompts'], prompts['name']):
                start = time()
                indexes = model.get_by_prompt(prompt)
                times.append(time()-start)

                if data.loc[indexes[0]]['name'] == name:
                    correct+=1
            
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
            data = pd.read_csv(self.cwbd / 'image' / benhmark['data'], index_col=0)
            test_data = pd.read_csv(self.cwbd / 'image' / benhmark['test_data'], index_col=0)

            correct = 0
            times = []
            for i, image, name in zip(test_data.index, test_data['img'], test_data['name']):
                start = time()
                image = CLIP.decode_image(image)
                indexes = model.get_by_image(image)

                times.append(time()-start)

                index = indexes[0] if indexes[0] != i else indexes[1]
                if index not in data.index: continue # Заменить когда буду прикручивать новую БД

                if data.loc[index]['name'] == name:
                    correct+=1

            mean_time = sum(times) / len(times)
            times_bench.append(mean_time)
            accuracy = (correct / len(test_data)) * 100
            mean_accuracy.append(accuracy)

            logging.getLogger().info(f"{benhmark['benchmark_name']} {mean_time:.4f} s {accuracy:.2f} %")
        logging.getLogger().info(f"Общий результат {sum(times_bench) / len(times_bench):.4f} s {sum(mean_accuracy)/len(mean_accuracy):.2f} %")
            