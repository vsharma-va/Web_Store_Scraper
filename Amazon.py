import csv
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Firefox()

url = "https://www.amazon.com"
#driver.get(url)

def create_url(phone_name):
    template = "https://www.amazon.com/s?k={}&ref=nb_sb_noss_2"
    search_item = phone_name.replace(' ', '+')
    url = template.format(search_item)
    return url

soup = BeautifulSoup(driver.page_source, 'html.parser')
# first try and get the entire row of data
# then try and get the name and price
# go from bigger to smaller
results = soup.find_all('div', {'data-component-type':'s-search-result'})  # find all div tags with a
# data-component-type = s-search-result

# for one product (prototype)
item = results[0]
product_name = item.h2.a
print(product_name.text)