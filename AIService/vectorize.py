import ruclip
import torch
from PIL import Image
from io import BytesIO
import numpy as np
import base64
import pandas as pd
from pymilvus import MilvusClient, DataType


client = MilvusClient('milvus.db')


def __decode_image(bs4):
    img = Image.open(BytesIO(base64.b64decode(bs4)))
    return img


def __decode_images(images: list):
    result = [__decode_image(bs4url) for bs4url in images]
    return result


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
__model, __processor = ruclip.load("ruclip-vit-base-patch32-384", device=device)
__predictor = ruclip.Predictor(__model, __processor, device=device, bs=8, templates=['{}', 'это {}', 'на фото {}'])


data = pd.read_csv('./Tests/Benchmarks/text/Irk_images.csv.xz')
images = __decode_images(data['img'])
with torch.no_grad():
    images_latents = __predictor.get_image_latents(images).cpu().detach().numpy()
    text_latents = __predictor.get_text_latents(data['name']).cpu().detach().numpy()


latents = np.concatenate((images_latents, text_latents), axis=1)
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