from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

# keyword_list = ['ipad']
headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
def discover_product_urls(url):
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_urls = []

    for product_link in soup.find_all('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'):
        product_url = urljoin(url, product_link.get('href'))
        product_urls.append(product_url)

    return product_urls

amazon_search_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'
product_urls = discover_product_urls(amazon_search_url)
print(f"Product URLs for':")
file=open('url.txt','a')
for url in product_urls:
    print(url)
    file.write(url+'\n')
