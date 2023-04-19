"""
Ülesanne B

Programm, mis teostab iga vähe aja tagant mitmesse enda valitud müügiportaali
(kaup24, osta, soov, amazon, e-bay, photopoint, arvutitark jne.) kasutaja etteantud otsingu.
Minimaalselt kuvab lingitud tulemusi (nimetus, hind, sait jne.).

Kasutamine: Pane programm käia ja sisesta toode, mille kohta soovid saada infot.

Kulutatud aeg: umbes 2 tundi

Author: Anton Kolisnetsenko
Date: 17.04.2023
"""

import requests
from bs4 import BeautifulSoup
import time


def search(portal, search_query):
    if portal == "okidoki":
        url = f"https://www.okidoki.ee/buy/all/?query={search_query}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("li", class_="classifieds__item")
        for item in items:
            title = item.find("a", class_="horiz-offer-card__title-link").text.strip()
            if len(title) > 40:
                title = title[:40 - 3] + "..."
            price_span = item.find("span", class_="horiz-offer-card__price-value")
            price = price_span.text.strip() if price_span else ""
            link = item.find("a", class_="horiz-offer-card__title-link")["href"]
            print("{:<40} {:>10} {}".format(title, price, "https://www.okidoki.ee" + link))
            '''result = {"title": title, "price": price, "link": link}
            results.append(result)'''
    elif portal == "kaup24":
        url = f"https://kaup24.ee/et/search?q={search_query}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("div", class_="product-list-item")
        for item in items:
            title = item.find("p", class_="product-name").text.strip()
            if len(title) > 40:
                title = title[:40 - 3] + "..."
            link = item.find("p", class_="product-name").find("a")["href"]
            price_span = item.find("span", class_="price")
            price = price_span.text.strip() if price_span else ""
            price = price[:-4] + "," + price[-4:]
            print("{:<40} {:>10} {}".format(title, price, "https://kaup24.ee" + link))
            '''result = {"title": title, "link": link, "price": price}
            results.append(result)'''
    elif portal == "photopoint":
        url = f"https://www.photopoint.ee/search?search_query={search_query}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("div", class_="single-product")
        for item in items:
            title = item.find("a", class_="link1").text.strip()
            if len(title) > 40:
                title = title[:40 - 3] + "..."
            link = item.find("a", class_="single-product-image")["href"]
            price_span = item.find("span", class_="show-reservations")
            price = price_span.text.strip() if price_span else ""
            print("{:<40} {:>10} {}".format(title, price, link))
            '''result = {"title": title, "link": link, "price": price}
            results.append(result)'''


websites = ["kaup24", "okidoki", "photopoint"]

if __name__ == "__main__":
    product = input("Enter the name of the product: ")

    while True:
        print("{:<40} {:>10} {}".format("Title", "Price", "Link"))

        for website in websites:
            search(website, product)

        time.sleep(120)
