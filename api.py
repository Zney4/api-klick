import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import logging


def shorten_link(bitly_token, long_url):
    url = "https://api-ssl.bitly.com/v4/bitlinks"
    authorization = {"Authorization": "Bearer {}".format(bitly_token)}
    params = {"long_url": long_url}
    response = requests.post(url, headers=authorization, json=params)
    response.raise_for_status()

    return response.json()["id"]


def count_clicks(bitly_token, bitlink):
    authorization = {"Authorization": "Bearer {}".format(bitly_token)}
    link = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    params = {"units": -1, "unit": "month"}
    response = requests.get(link, params=params, headers=authorization)
    response.raise_for_status()

    return response.json()["total_clicks"]


def is_bitlink(long_url, bitly_token):
    authorization = {"Authorization": "Bearer {}".format(bitly_token)}
    info_url = f"https://api-ssl.bitly.com/v4/bitlinks/{long_url}"

    response = requests.get(info_url, headers=authorization)

    return response.ok


def get_parsed_url(bitlink):
    parsed_bitlink = urlparse(bitlink)

    return f"{parsed_bitlink.netloc}{parsed_bitlink.path}"


if __name__ == "__main__":
    load_dotenv()
    bitly_token = os.environ["BITLY_TOKEN"]

    long_url = input("Введите ссылку \n>>>")

    try:
        status_code = is_bitlink(long_url, bitly_token)
        logging.info("info_url:", status_code)
        if status_code:
            count_clicks = count_clicks(bitly_token, long_url)
            print("Колличество кликов:", count_clicks)
        else:
            bitlink = shorten_link(bitly_token, long_url)
            parsed_path_bitlink = get_parsed_url(bitlink)
            print("Битлинк", parsed_path_bitlink)

    except requests.exceptions.HTTPError as ex:
        print(ex)
