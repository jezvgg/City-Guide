from Model import CLIP
from flask import request
from connexion import FlaskApp
import json


app = FlaskApp(__name__)

model = CLIP('milvus.db')


@app.route('/get_by_prompt/<city>', methods=['POST'])
def service_prompt(city: str):
    args = request.json

    indexes = model.get_by_prompt(str(args['prompt']), city)

    result = [{'id':index['id']} | index['entity'] for index in indexes[0]]

    return result


@app.route('/get_by_image/<city>', methods=['POST'])
def service_image(city: str):
    args = request.data

    image = CLIP.decode_binary(args)
    indexes = model.get_by_image(image, city)

    result = [{'id':index['id']} | index['entity'] for index in indexes[0]]
    return result


if __name__ == "__main__":
    app.add_api('swagger.yml')
    app.run()
