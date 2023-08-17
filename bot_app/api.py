import requests

import settings
from settings import DOMAIN, ENDPOINT
from . import functions


def get_csv(distributor_name):
    url = f"{DOMAIN}/{ENDPOINT}/csv/{distributor_name}"
    csv_req = requests.get(url)
    if csv_req.status_code == 200:
        response = csv_req.json()
        csv_url = f"{settings.DOMAIN}/{response['csv']}"
        response = requests.get(
            url=csv_url,
        )
        file_name = csv_url.split("/")[-1]
        file_path = f"media/csv/{distributor_name}/{file_name}"
        file = open(file_path, "wb")
        file.write(response.content)
        file.close()

        return file_path
    else:
        return ""


def upload_csv(file_path, distributor_name, chat_id):
    # FILE
    file_url = f"https://api.telegram.org/file/bot{settings.API_KEY}/{file_path}"
    file_response = requests.get(file_url)
    current_date = functions.get_current_date()
    files = {"csv": (f"{distributor_name}_{current_date}.csv", file_response.content)}

    # API URL
    url = f"{DOMAIN}/{ENDPOINT}/document/{distributor_name}/parse"
    data = {
        "chat_id": chat_id,
    }
    response = requests.post(
        url,
        data=data,
        files=files,
    )
    return response
