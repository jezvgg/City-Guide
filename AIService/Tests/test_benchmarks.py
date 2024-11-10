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
        model = CLIP('milvus.db')
        times_bench = []
        mean_accuracy = []
        for benhmark in self.prompt_test:
            prompts = pd.read_csv(self.cwbd / 'text' / benhmark['prompts'])
            data = pd.read_csv(self.cwbd / 'text' / benhmark['data'])

            correct = 0
            times = []
            for prompt, name in zip(prompts['prompts'], prompts['name']):
                start = time()
                indexes = model.get_by_prompt(prompt, benhmark['index'])
                times.append(time()-start)

                if indexes[0][0]['entity']['name'] == name:
                    correct+=1
            
            mean_time = sum(times) / len(times)
            times_bench.append(mean_time)
            accuracy = (correct / len(prompts)) * 100
            mean_accuracy.append(accuracy)

            logging.getLogger().info(f"{benhmark['benchmark_name']} {mean_time:.4f} s {accuracy:.2f} %")
        logging.getLogger().info(f"Общий результат {sum(times_bench) / len(times_bench):.4f} s {sum(mean_accuracy)/len(mean_accuracy):.2f} %")


    def test_getting_by_image(self):
        model = CLIP('milvus.db')
        times_bench = []
        mean_accuracy = []

        for benhmark in self.images_test:
            print('\n',benhmark['benchmark_name'])
            data = pd.read_csv(self.cwbd / 'image' / benhmark['data'])
            test_data = pd.read_csv(self.cwbd / 'image' / benhmark['test_data'])

            correct = 0
            times = []
            for i, image, name in zip(test_data['guid'], test_data['img'], test_data['name']):
                start = time()
                image = CLIP.decode_image(image)
                indexes = model.get_by_image(image, benhmark['index'])
                times.append(time()-start)

                with open("example.json", 'w') as f: json.dump(indexes[0], f, indent=4, ensure_ascii=False)

                index_name = indexes[0][0]['entity']['name'] if indexes[0][0]['id'] != i else indexes[0][1]['entity']['name']

                if index_name == name:
                    correct+=1

            mean_time = sum(times) / len(times)
            times_bench.append(mean_time)
            accuracy = (correct / len(test_data)) * 100
            mean_accuracy.append(accuracy)

            logging.getLogger().info(f"{benhmark['benchmark_name']} {mean_time:.4f} s {accuracy:.2f} %")
        logging.getLogger().info(f"Общий результат {sum(times_bench) / len(times_bench):.4f} s {sum(mean_accuracy)/len(mean_accuracy):.2f} %")
            