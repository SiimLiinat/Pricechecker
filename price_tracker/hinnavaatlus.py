"""
https://hinnavaatlus.ee price tracker.
"""

# TODO Running in background
# TODO Schedule

# TODO Ability to save over price point
# TODO Notification system

# TODO Saving data over longer time
# TODO Plotting data

import bs4
import requests

webpages = {"https://www.hinnavaatlus.ee/search/?query=ryzen+3600&min_price=&max_price=": 200}


def get_price(url: str):
    """Get price of product."""
    result = requests.get(url)
    soup = bs4.BeautifulSoup(result.text, 'html.parser')
    name = soup.select('li.product-list-item:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > a:nth-child(1) > span:nth-child(1)')
    price = soup.select('li.product-list-item:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > p:nth-child(1) > span:nth-child(1)')
    # return f'{name[0].text} - {float(price[0].text.replace(" €", "").replace(",", "."))}'
    return name[0].text, float(price[0].text.replace(" €", "").replace(",", ".")),


print("Deals:")

for site in webpages:
    name, price = get_price(site)
    if webpages[site] == 0:
        webpages[site] = price
    elif price <= webpages[site]:
        webpages[site] = price
        print(f"{name} - {price}. Direct link: {site}")

print("Complete.")
