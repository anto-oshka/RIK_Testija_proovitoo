"""
Kohustuslik ülesanne

Kirjutada spider, mis leiab rekursiivselt kõik lingid www.rik.ee lehel
ning tagastab urlide kõikide HTTP meetodite vastuste kohta raporti.
Alamdomeenid pole skoobis. Ärge tehke koormustesti või DDOSi.

Tulem võiks olla minimaalselt: spider väljund (Meetod, URL, vastus, content-length ja muu mis tundub mõttekas) +
Järeldused (Mis said teada tehnoloogiate kohta, mis HTTP päised on üle või puudu ja muud tähelepanekud).

Author: Anton Kolisnetsenko
Date: 09.04.2023
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = set()
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and not href.startswith("#"):
            link_url = urljoin(url, href)
            link_domain = urlparse(link_url).netloc
            if link_domain == "www.rik.ee":
                links.add(link_url)
    return links


def get_response_data(url, method):
    response = requests.request(method, url)
    status_code = response.status_code
    headers = response.headers
    content_length = headers.get("content-length")
    return method, url, status_code, content_length, headers


def spider(url):
    links = get_links(url)
    response_data = []
    for link in links:
        response_data.append(get_response_data(link, "GET"))
        response_data.append(get_response_data(link, "HEAD"))
        response_data.append(get_response_data(link, "OPTIONS"))

    return response_data


if __name__ == "__main__":
    url = "https://www.rik.ee"
    response_data = spider(url)
    for data in response_data:
        method, url, status_code, content_length, headers = data
        print(method, url, status_code, content_length)
