import requests
from bcb import sgs


def get_selic_rate():
    url = (
        "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        latest_rate = data[-1]["valor"]
        return float(latest_rate)
    else:
        return None


def get_ipca_rate():
    ipca_data = sgs.get({"ipca": 433})
    if not ipca_data.empty:
        return ipca_data.iloc[0]["ipca"]
    return None
