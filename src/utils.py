from config import Vars, Errors
import io
from models.plate_reader import PlateReader, InvalidImage
import logging
import requests


def check_image_id(image_id: str) -> bool:
    '''
    Function for validating image id
    '''
    if not isinstance(image_id, str) or not image_id.isdecimal() or \
            image_id not in Vars.AVAILABLE_IDS or image_id[0] == '0':
        return False
    return True


def get_image(image_id: int) -> bytes | tuple:
    '''
    Function to get image or return error by id from server url
    '''
    image = requests.get(f'{Vars.IMAGE_SERVER}/{image_id}', timeout=5)
    if image.status_code // 100 == 2:
        return image.content
    elif image.status_code // 100 == 5:
        logging.error(Errors.SERVER_ERROR)
        return {'error': Errors.SERVER_ERROR}, 500
    elif image.status_code // 100 == 4:
        logging.error(Errors.IMAGE_NOT_FOUND)
        return {'error': Errors.IMAGE_NOT_FOUND}, 404
    else:
        logging.error(Errors.SERVER_ERROR)
        return {'error': Errors.SERVER_ERROR}, 500


def plate_reader_by_id(plate_reader: PlateReader, image_id: str) -> str | tuple:
    '''
    Function for validate errors and then return plate number by ID
    '''
    if not check_image_id(image_id):
        return {'error': Errors.INVALID_ID}, 400
    image = get_image(int(image_id))
    if isinstance(image, str):
        return image
    image = io.BytesIO(image)
    try:
        res = plate_reader.read_text(image)
        return res
    except InvalidImage:
        logging.error(Errors.INVALID_IMAGE)
        return {'error': Errors.INVALID_IMAGE}, 400


def json_handler(keys: list, values: list) -> dict | tuple:
    '''
    Function for convertation two lists to json dict
    '''
    if len(keys) != len(values):
        logging.error(Errors.JSON_ERROR)
        return {'error': Errors.JSON_ERROR}, 500
    return {keys[i]: values[i] for i in range(len(keys))}
