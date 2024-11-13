import json

from flask import request
from connexion import FlaskApp

from Model import ruCLIP
from service import service
from pymilvus import MilvusClient


app = FlaskApp(__name__)


with open("milvus_conf.json") as f:
    database_client = MilvusClient(**json.load(f))
model = ruCLIP()
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
    app.run()
