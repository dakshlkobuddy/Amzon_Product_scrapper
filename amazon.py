from selectorlib import Extractor
import requests 
import json
import csv
from time import sleep
import sys



# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('search_results.yml')
pages_scraped = 0
def scrape(url):  

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

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    return e.extract(r.text)

# product_data = []
fields=['url','name','price','rating','number_of_reviews']
with open("search_results_urls.txt", 'r') as urllist, open('search_results_output.csv', 'a') as outfile:
    csvwriter=csv.writer(outfile)
    csvwriter.writerow(fields)
    for url in urllist.read().splitlines():
        # Check if we've scraped 20 pages, if so, exit the loop
        if pages_scraped >= 20:
            break

        data = scrape(url)
        if data:
            for product in data['products']:
                product['search_url'] = url
                # product_data = {
                #     'url': product['url'],
                #     'name': product['title'],
                #     'price': product['price'],
                #     'rating': product['rating'],
                #     'number_of_reviews': product['number_of_reviews']
                # }
                # print("Saving Product: %s" % product['title'])
                # json.dump(product_data, outfile)
                # outfile.write("\n")
                # outfile.write("]")
                csv_data=[product['url'],product['title'],product['price'],product['rating'],product['number_of_reviews']]
                print(csv_data)
                csvwriter.writerow(csv_data)

        # Increment the pages_scraped counter
        pages_scraped += 1