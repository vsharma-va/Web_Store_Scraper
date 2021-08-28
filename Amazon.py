import Amazon_Functions
import csv
import os
from bs4 import BeautifulSoup
from selenium import webdriver


def main():
    driver = webdriver.Firefox()
    term_to_search = input("Enter the search term")
    url = Amazon_Functions.Create_Url(term_to_search)

    for page in range(1, 3):
        actual_price = []
        discounted_price = []
        device_names = []
        hovered_items = []
        hovered_price_actual = []
        hovered_price_discount = []
        amazons_items = []
        amazons_price_actual = []
        amazons_price_discount = []
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        total_products_on_page = len(results)
        for i in range(total_products_on_page):
            print(i)
            item = results[i]

            if (Amazon_Functions.Check_Amazons_Choice(item)):
                item_name_choice = item.h2.a.span
                item_name_choice_text = item_name_choice.text
                amazons_items.append(item_name_choice_text)
                price = Amazon_Functions.Return_Discount_Actual_Price(item)
                amazons_price_actual.append(price[1])
                amazons_price_discount.append(price[0])
                continue

            if (Amazon_Functions.Check_Hovered_Sponsor(item)):
                item_name_hovered = item.h2.a.span
                item_name_hovered_text = item_name_hovered.text
                hovered_items.append(item_name_hovered_text)
                price = Amazon_Functions.Return_Discount_Actual_Price(item)
                hovered_price_actual.append(price[1])
                hovered_price_discount.append(price[0])
                continue

            try:
                item_name = item.h2.a.span
                device_names.append(item_name.text)
            except AttributeError:
                print("No Name")

            price = Amazon_Functions.Return_Discount_Actual_Price(item)
            if price[1]:
                actual_price.append(price[1])
            if price[0]:
                discounted_price.append(price[0])

        remaining_records = Amazon_Functions.Delete_Amazon_Or_Hovered(hovered_items, hovered_price_discount,
                                                                      hovered_price_actual,
                                                                      amazons_items, amazons_price_actual,
                                                                      amazons_price_discount)

        hovered_items = remaining_records[0][0]
        hovered_price_actual = remaining_records[0][1]
        hovered_price_discount = remaining_records[0][2]

        amazons_items = remaining_records[1][0]
        amazons_price_actual = remaining_records[1][1]
        amazons_price_discount = remaining_records[1][2]

        final_records = Amazon_Functions.Add_Amazon_Or_Hovered_Items(hovered_items, amazons_items, device_names,
                                                                     actual_price, discounted_price,
                                                                     amazons_price_discount,
                                                                     amazons_price_actual, hovered_price_actual,
                                                                     hovered_price_discount)

        device_names = final_records[0]
        actual_price = final_records[1]
        discounted_price = final_records[2]

        Amazon_Functions.Write_To_CSV(device_names, actual_price, discounted_price)


if __name__ == '__main__':
    main()
