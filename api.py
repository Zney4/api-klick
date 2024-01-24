import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(bitlink_token, long_url):
    url = "https://api-ssl.bitly.com/v4/bitlinks"
    Authorization_my_new_var = {"Authorization": "Bearer {}".format(bitlink_token)}
    params = {"long_url": long_url}
    response = requests.post(url, headers=Authorization_my_new_var, json=params)
    response.raise_for_status()

    return response.json()["id"]


def count_clicks(bitlink_token, bitlink):
    Authorization_my_new_var = {"Authorization": "Bearer {}".format(bitlink_token)}
    link = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    params = {"units": -1, "unit": "month"}
    response = requests.get(link, params=params, headers=Authorization_my_new_var)
    response.raise_for_status()

    return response.json()["total_clicks"]


def is_bitlink(long_url, bitlink_token):
    Authorization_my_new_var = {"Authorization": "Bearer {}".format(bitlink_token)}
    info_url = f'https://api-ssl.bitly.com/v4/bitlinks/{long_url}'

    response = requests.get(info_url, headers=Authorization_my_new_var)

    return response.status_code


def parsed_url(bitlink):
    parsed_bitlink = urlparse(bitlink)

    return f'{parsed_bitlink.netloc}{parsed_bitlink.path}'


if __name__ == "__main__":
    load_dotenv()
    bitlink_token = os.environ["BITLINK_TOKEN"]

    long_url = input("Введите ссылку \n>>>")

    status_code = is_bitlink(long_url, bitlink_token)
    print('info_url:', status_code)

    try:
        if status_code == 200:
            count_clicks = count_clicks(bitlink_token, long_url)
            print("Колличество кликов:", count_clicks)
        else:
            bitlink = shorten_link(bitlink_token)
            count_clicks = count_clicks(bitlink_token, long_url)
            print("Колличество кликов:", count_clicks)

    except requests.exceptions.HTTPError as ex:
        print(ex)
        print("Битлинк", bitlink)

        parsed_path_bitlink = parsed_url(bitlink)
