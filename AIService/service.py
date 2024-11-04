from CLIP import CLIP
from flask import Flask, request


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
model = CLIP('irkutsk.index')


towns = {'nino':'niznii_novgorod.index',
         'yaros':'yaroslavl.index',
         'vlad':'vladimir.index',
         'ekb':'ekaterinburg.index'}


@app.route('/get_by_prompt/<city>', methods=['GET','POST'])
def service_prompt(city):
    args = request.form
    model.set_index(towns[city])

    indexes = model.get_by_prompt(str(args['prompt']))

    return app.response_class(
            response='['+','.join(map(str, indexes))+']',
            status=200,
            mimetype="text"
        )


@app.route('/get_by_image/<city>', methods=['GET','POST'])
def service_image(city):
    args = request.data
    model.set_index(towns[city])

    image = CLIP.decode_binary(args)
    indexes = model.get_by_image(image)

    return app.response_class(
            response='['+','.join(map(str, indexes))+']',
            status=200,
            mimetype="text"
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
