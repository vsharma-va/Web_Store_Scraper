import csv
import Flipkart_Functions
import os
from bs4 import BeautifulSoup
from selenium import webdriver


def main():
    driver = webdriver.Firefox(executable_path=r"../Resources/geckodriver.exe")
    term_to_search = input("Enter the search term")
    max_pages = int(input("Enter the number of pages you want to search"))
    url = Flipkart_Functions.Create_Url(term_to_search, max_pages)

    for page in (1, max_pages+1):
        driver.get(url)
        device_name = []
        device_price_actual = []
        device_price_discounted = []
        device_info = []
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('a', {'target': '_blank'})
        total_results = soup.find('span', {'class': '_10Ermr'})
        total_results_list = total_results.text.split(' ')
        print(total_results_list[3])
        for i in range(int(total_results_list[3])):
            item = results[i]
            product_name = Flipkart_Functions.Get_Product_Name(item)
            product_price_actual = Flipkart_Functions.Get_Product_Actual_Price(item)
            product_price_discounted = Flipkart_Functions.Get_Product_Discounted_Price(item)
            product_specifications = Flipkart_Functions.Get_Product_Specifications(item)

            device_name.append(product_name)
            device_price_actual.append(product_price_actual)
            device_price_discounted.append(product_price_discounted)
            device_info.append(product_specifications)

        Flipkart_Functions.Write_To_CSV(device_name, device_price_actual, device_price_discounted, device_info)


if __name__ == '__main__':
    main()
    print("Finished")