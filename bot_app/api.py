import datetime

import requests

import settings
from settings import DOMAIN, ENDPOINT


def get_csv(distributor_name):
    url = f"{DOMAIN}/{ENDPOINT}/csv/{distributor_name}"
    csv_req = requests.get(url)
    if csv_req.status_code == 200:
        response = csv_req.json()
        csv_url = f"{settings.DOMAIN}/{response['csv']}"
        response = requests.get(
            url=csv_url,
        )
        current_date = datetime.date.today()
        file_path = f"media/csv/{distributor_name}/{distributor_name}_{current_date}.csv"
        file = open(file_path, "wb")
        file.write(response.content)
        file.close()

        return file_path
    else:
        return ""


def upload_csv(file_path, distributor_name, chat_id):
    file_url = f"https://api.telegram.org/file/bot{settings.API_KEY}/document/{file_path}"
    with open(file_url, "r") as file:
        url = f"{DOMAIN}/{ENDPOINT}/document/{distributor_name}/parse"
        data = {
            "chat_id": chat_id,
        }
        file_data = {
            "csv": (file_url, file),
        }
        upload_req = requests.post(
            url,
            data=data,
            files=file_data,
        )
    print(upload_req)
    return upload_req
