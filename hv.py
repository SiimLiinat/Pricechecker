"""
https://hinnavaatlus.ee price tracker.
"""

# TODO Running in background
# TODO Schedule (run at certain times)

# TODO Ability to save over price point
# TODO Notification system (email etc)

# TODO Filter data based on item

# TODO Plot multiple items at the same time

from datetime import datetime
import bs4
import json
import matplotlib.pyplot as plt
import requests

webpages = {"https://www.hinnavaatlus.ee/search/?query=ryzen+3600&min_price=&max_price=": 200,
            "https://www.hinnavaatlus.ee/products/Arvutikomponendid/Videokaardid/6c1d391955a7127779cba8cb35a29175"
            "/?sort=-views": 300}


def get_price(url: str):
    """Get price of product."""
    result = requests.get(url)
    soup = bs4.BeautifulSoup(result.text, 'html.parser')
    name = soup.select(
        'li.product-list-item:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child('
        '2) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > a:nth-child(1) > span:nth-child(1)')
    price = soup.select(
        'li.product-list-item:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child('
        '2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > p:nth-child(1) > span:nth-child(1)')
    return name[0].text, float(price[0].text.replace(" €", "").replace(",", ".")),


def save_data(item, cost):
    """Save item name, cost and current time in JSON format to .txt file."""
    py_data = [item, cost, datetime.now().strftime("%Y/%m/%d")]
    data = json.dumps(py_data)
    with open("collected_data.txt", "a") as f:
        json.dump(data, f)
        f.write("\n")


def get_data():
    """Returns JSON data from .txt file."""
    with open("collected_data.txt", "r"):
        data = [json.loads(json.loads(line)) for line in open('collected_data.txt', 'r')]
    return data


def plot_graph():
    #data = get_data()
    #plt.plot()
    #for site in webpages:
    #    name, price = get_price(site)
    #    item_data = list(filter(lambda x: x[0] == name, data))
    #    name_1, price, date = [*zip(*item_data)]
    #    plt.plot(date, price, label=name)
    #plt.legend()
    #plt.show()

    data = get_data()
    names = set(x[0] for x in data)
    (names)  # graph brakes without mentioning names
    for name in names:
        item_data = list(filter(lambda x: x[0] == name, data))
        name_1, price, date = [*zip(*item_data)]
        plt.plot(date, price, label=name)
    plt.legend()
    plt.show()


def return_info():
    """Return deals."""
    print("Deals:\n")

    for site in webpages:
        name, price = get_price(site)
        save_data(name, price)
        if webpages[site] == 0:
            webpages[site] = price
        elif price <= webpages[site]:
            webpages[site] = price
            print(f"{name} - {price}. Direct link: {site}")

    return "\nComplete."


print(return_info())
plot_graph()
