import json

from flask import request
from connexion import FlaskApp

from Model import ONNX_CLIP, ruCLIP_proccesor
from service import service
from pymilvus import MilvusClient


app = FlaskApp(__name__)


with open("milvus_conf.json") as f: database_config = json.load(f)
with open("processor_config.json") as f: processor_config = json.load(f)
with open("model_config.json") as f: model_config = json.load(f)
    
database_client = MilvusClient(**database_config)
proccesor = ruCLIP_proccesor(**processor_config)
model = ONNX_CLIP(proccesor, **model_config)
main_service = service(database_client, model)


@app.route('/get_by_prompt/<city>', methods=['POST'])
def service_prompt(city: str):
    args = request.json

    result = main_service.get_by_prompt(str(args["prompt"]), city)

    return main_service.create_reponse(result)


@app.route('/get_by_image/<city>', methods=['POST'])
def service_image(city: str):
    args = request.data

    image = service.decode_binary(args)
    result = main_service.get_by_image(image, city)

    return main_service.create_reponse(result)


if __name__ == "__main__":
    app.add_api('swagger.yml')
    app.run(port='0.0.0.0')
