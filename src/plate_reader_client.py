import requests
from typing import Any


class PlateReaderClient:
    def __init__(self, host: str):
        self.host = host

    def read_plate_id(self, image_id: str) -> dict[str]:
        res = requests.post(
            f'{self.host}/ReadImgId',
            headers={'Content-Type': 'application/json'},
            json={'id': image_id},
        )
        return res.json()

    def read_plate_ids(self, image_ids: list[Any]) -> dict[str]:
        res = requests.post(
            f'{self.host}/ReadImgIds',
            headers={'Content-Type': 'application/json'},
            json={'id': image_ids},
        )
        return res.json()


if __name__ == '__main__':
    client = PlateReaderClient(host='http://127.0.0.1:8080')
    res = client.read_plate_ids(['1', '9965', 4, '10022', [24234], '231290', 10022])
    print(res)
