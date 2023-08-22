# importing libraries
from bs4 import BeautifulSoup
import requests
import json

def main(URL):
    # opening our output file in append mode
    File = open("out.csv", "a")
    # specifying user agent, You can use other user agents
    # available on the internet
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'})
    # Making the HTTP Request
    webpage = requests.get(URL, headers=HEADERS)
    # Creating the Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")
    # retrieving product title
    try:
        # Outer Tag Object
        title = soup.find("span",attrs={"id": 'productTitle'})
        # Inner NavigableString Object
        title_value = title.string
        # Title as a string value
        title_string = title_value.strip().replace(',', '')
    except AttributeError:
        title_string = "NA"
    print("product Title = ", title_string)
    # saving the title in the file
    File.write(f"{title_string},")
    # retrieving price

    try:
        desc_element = soup.find('ul',{'class':"a-unordered-list a-vertical a-spacing-mini"}).text
        # we are omitting unnecessary spaces
        # and commas form our string
    except AttributeError:
        desc_element = "NA"
    print("Decription = ", desc_element)
    
    File.write(f"{desc_element},")

    try:
        asin_element = soup.find('input',{'name':'ASIN'})
        # we are omitting unnecessary spaces
        # and commas form our string
    except AttributeError:
        asin_element = "NA"
    print("ASIN = ", asin_element['value'])
    # saving
    File.write(f"{asin_element['value']},")

    try:
        manufacturer_element = soup.find('a',{'id':'bylineInfo'})
        if manufacturer_element:
            manufacturer=manufacturer_element.get_text(strip=True)[10:]
        # we are omitting unnecessary spaces
        # and commas form our string
    except AttributeError:
        manufacturer_element = "NA"
    print("Manufacturer = ", manufacturer)
    # saving
    File.write(f"{manufacturer},")
    # retrieving product rating
    # try:
    #     rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip().replace(',', '')
    # except AttributeError:
    #     try:
    #         rating = soup.find(
    #             "span", attrs={'class': 'a-icon-alt'}).string.strip().replace(',', '')
    #     except:
    #         rating = "NA"
    # print("Overall rating = ", rating)
    # File.write(f"{rating},")
    # try:
    #     review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip().replace(',', '')
    # except AttributeError:
    #     review_count = "NA"
    # print("Total reviews = ", review_count)
    # File.write(f"{review_count},")
    # print availablility status
    try:
        prod_desc_element = soup.find("div", attrs={'id': 'productDescription'})
        prod_desc=prod_desc_element.get_text(strip=True) if prod_desc_element else "Description not Found"
    except AttributeError:
        prod_desc = "NA"
    print("Product Description = ", prod_desc)
    # saving the availability and closing the line
    File.write(f"{prod_desc},\n")
    # closing the file
    File.close()
if __name__ == '__main__':# opening our url file to access URLs
    file = open("url.txt",'r')
    for url in file.read().splitlines():
    # iterating over the urls
        # print(url)
        main(url)