from dataclasses import dataclass


@dataclass
class Errors:
    ID_NOT_FOUND = 'Didn\'t find image id'
    INVALID_ID = 'Invalid image ID'
    INVALID_IMAGE = 'Invalid image'
    IMAGE_NOT_FOUND = 'Image with this id didn\'t find'
    SERVER_ERROR = 'Problem with images server'
    JSON_ERROR = 'Inavlid params to json convert'


@dataclass
class Vars:
    IMAGE_SERVER = 'http://178.154.220.122:7777/images/'
    AVAILABLE_IDS = ['10022', '9965']
