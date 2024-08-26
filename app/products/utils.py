from retrying import retry

from bs4 import BeautifulSoup
import requests
from fastapi import HTTPException
from fastapi import status as http_status

def retry_if_connection_error(exception):
        return isinstance(exception, ConnectionError)

@retry(retry_on_exception=retry_if_connection_error, wait_fixed=2000)
def get_html(url: str) -> BeautifulSoup:
    response = requests.get(url)
    text = response.content

    if response.status_code == 200:
        html = BeautifulSoup(markup=text, features="lxml")

        return html

    raise HTTPException(status_code=http_status.HTTP_501_NOT_IMPLEMENTED,
                        detail=f"Scraper didn't succeed in getting data:\n"
                            f"\turl: {url}\n"
                            f"\tstatus code: {response.status}\n"
                            f"\tresponse text: {text}")

def log_in_console(message):
    print('<<-------------------------------->> ', message, " <<-------------------------------->>")
    return