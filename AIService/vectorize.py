from PIL import Image
from io import BytesIO
import numpy as np
import base64
import pandas as pd
from pymilvus import MilvusClient, DataType

import json
from Model import ONNX_CLIP, ruCLIP_proccesor


client = MilvusClient('milvus.db')


def __decode_image(bs4):
    img = Image.open(BytesIO(base64.b64decode(bs4)))
    return img


def __decode_images(images: list):
    result = [__decode_image(bs4url) for bs4url in images]
    return result


with open("milvus_conf.json") as f:
    database_client = MilvusClient(**json.load(f))
proccesor = ruCLIP_proccesor('proccesor_config.json')
model = ONNX_CLIP(proccesor, 'clip_textual.onnx', 'clip_visual.onnx')


data = pd.read_csv('./Tests/Benchmarks/text/Irk_images.csv.xz')
images = __decode_images(data['img'])

datas = []
imagess = []
for dat, image in zip(data['name'], images):
    imagess.append(model.get_image_latents(image)[0])
    datas.append(model.get_text_latents(dat)[0])

images_latents = np.array(imagess)
text_latents = np.array(datas)
print(images_latents)
latents = np.concatenate((images_latents, text_latents), axis=1).astype(np.float64)
print(latents)
dimensions = latents[0].size

data.insert(0, 'vector', latents.tolist())

data.drop(columns=['img'], inplace=True)

schema = MilvusClient.create_schema(
    auto_id = False,
)
schema.add_field(field_name="guid", datatype=DataType.VARCHAR, is_primary=True, max_length=36 )
schema.add_field(field_name="name", datatype=DataType.VARCHAR, max_length=256 )
schema.add_field(field_name="description", datatype=DataType.VARCHAR, max_length=2048 )
schema.add_field(field_name="latitude", datatype=DataType.DOUBLE)
schema.add_field(field_name="longitude", datatype=DataType.DOUBLE)
schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=dimensions)

index_params = client.prepare_index_params()

index_params.add_index(field_name="guid")
index_params.add_index(field_name="name")
index_params.add_index(field_name="description")
index_params.add_index(field_name="latitude")
index_params.add_index(field_name="longitude")

index_params.add_index(
    field_name="vector", 
    index_type="FLAT",
    metric_type="COSINE",
    params={ "nlist": len(data['name'].unique()) }
)

client.create_collection(
    collection_name='Irkutsk',
    schema=schema,
    index_params=index_params
)

res = client.insert(
    collection_name='Irkutsk',
    data=data.to_dict('records')
)

print(res)

res = client.describe_collection(
    collection_name="Irkutsk"
)

print(res)