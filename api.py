import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(bitlink_token, long_url):
    url = "https://api-ssl.bitly.com/v4/bitlinks"
    authorization = {"Authorization": "Bearer {}".format(bitlink_token)}
    params = {"long_url": long_url}
    response = requests.post(url, headers=authorization, json=params)
    response.raise_for_status()

    return response.json()["id"]


<<<<<<< HEAD
def count_clicks(bitly_token, bitlink):
    authorization = {"Authorization": "Bearer {}".format(bitly_token)}
=======
def count_clicks(bitlink_token, bitlink):
    authorization = {"Authorization": "Bearer {}".format(bitlink_token)}
>>>>>>> 54eb4734c43e1821d79da1cb58ae8f0cd81b2e17
    link = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    params = {"units": -1, "unit": "month"}
    response = requests.get(link, params=params, headers=authorization)
    response.raise_for_status()

    return response.json()["total_clicks"]


<<<<<<< HEAD
def is_bitlink(long_url, bitly_token):
    authorization = {"Authorization": "Bearer {}".format(bitly_token)}
=======
def is_bitlink(long_url, bitlink_token):
    authorization = {"Authorization": "Bearer {}".format(bitlink_token)}
>>>>>>> 54eb4734c43e1821d79da1cb58ae8f0cd81b2e17
    info_url = f'https://api-ssl.bitly.com/v4/bitlinks/{long_url}'

    response = requests.get(info_url, headers=authorization)

    return response.status_code


def get_parsed_url(bitlink):
    parsed_bitlink = urlparse(bitlink)

    return f'{parsed_bitlink.netloc}{parsed_bitlink.path}'


if __name__ == "__main__":
    load_dotenv()
    bitly_token = os.environ["BITLINK_TOKEN"]

    long_url = input("Введите ссылку \n>>>")

    status_code = is_bitlink(long_url, bitly_token)
    print('info_url:', status_code)

    try:
        if status_code == 200:
            count_clicks = count_clicks(bitly_token, long_url)
            print("Колличество кликов:", count_clicks)
        else:
            bitlink = shorten_link(bitly_token, long_url)
            count_clicks = count_clicks(bitly_token, long_url)
            print("Колличество кликов:", count_clicks)

    except requests.exceptions.HTTPError as ex:
        print(ex)
        print("Битлинк", bitlink)

        parsed_path_bitlink = get_parsed_url(bitlink)
