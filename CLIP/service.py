from CLIP import CLIP
from flask import Flask, request


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
model = CLIP('irkutsk.index')


@app.route('/')
def service():
    args = request.args
    if 'image' in args:
        index = model.get_by_image(args['image'])
    elif 'prompt' in args:
        index = model.get_by_prompt(args['prompt'])

    return app.response_class(
            response=str(index),
            status=200,
            mimetype="text"
        )


if __name__ == "__main__":
    app.run()
