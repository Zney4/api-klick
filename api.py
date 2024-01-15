import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(url, api):
    headers = {"Authorization": "Bearer {}".format(api)}
    long_url = input("Введите ссылку \n>>>")
    params = {"long_url": long_url}
    response = requests.post(url, headers=headers, json=params)
    response.raise_for_status()

    return response.json()["id"]


def count_clicks(api, bitlink):
    headers = {"Authorization": "Bearer {}".format(api)}
    link = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    params = {"units": -1, "unit": "month"}
    response = requests.get(link, params=params, headers=headers)
    response.raise_for_status()

    print("Колличество кликов:", response.json()["total_clicks"])

    return response.json()["total_clicks"]


def parsed_url(bitlink):
    parsed_bitlink = urlparse(bitlink)

    return parsed_bitlink.netloc + parsed_bitlink.path


if __name__ == "__main__":
    load_dotenv()

    url = "https://api-ssl.bitly.com/v4/bitlinks"
    api = os.getenv("api")
    try:
        bitlink = shorten_link(url, api)
    except requests.exceptions.HTTPError as ex:
        print(ex)

    print("Битлинк", bitlink)

    parsed_path_bitlink = parsed_url(bitlink)
    count_clicks(api, parsed_path_bitlink)
