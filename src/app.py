from flask import Flask, request
import logging
from models.plate_reader import PlateReader
from utils import plate_reader_by_id, json_handler
from config import Errors


app = Flask(__name__)
plate_reader = PlateReader.load_from_file('./model_weights/plate_reader_model.pth')


@app.route('/')
def first_page() -> str:
    return '<h1><center>Hello!!!!!</center></h1>'


@app.route('/ReadImgId', methods=['POST'])
def read_plate_number_by_id() -> dict | tuple:
    if 'id' not in request.json:
        return {'error': Errors.ID_NOT_FOUND}, 400
    image_id = request.json['id']
    res = plate_reader_by_id(plate_reader, image_id)
    return json_handler(['plate_number'], [res])


@app.route('/ReadImgIds', methods=['POST'])
def read_plate_number_by_ids() -> dict | tuple:
    if 'id' not in request.json:
        return {'error': Errors.ID_NOT_FOUND}, 400
    image_ids = request.json['id']
    res = []
    for image_id in image_ids:
        res.append(plate_reader_by_id(plate_reader, image_id))
    return json_handler([f'plate_number_{i + 1}' for i in range(len(image_ids))], res)


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8080, debug=True)
