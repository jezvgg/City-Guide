from CLIP import CLIP
from flask import Flask, request
import pandas as pd


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
model = CLIP('photos_v3.csv.xz')


@app.route('/')
def service():
    args = request.args
    if 'image' in args:
        index = model.get_by_image(args['image'])
        return app.response_class(
            response=str(index),
            status=200,
            mimetype="text"
        )

    elif 'prompt' in args:
        img, index = model.get_by_prompt(args['prompt'])
        return app.response_class(
            response=str(index),
            status=200,
            mimetype="text"
        )


if __name__ == "__main__":
    app.run()
