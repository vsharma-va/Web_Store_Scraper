import os
import csv


def Create_Url(search_item):
    template = "https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    page_url = template.format(search_item)
    page_url += "&page={}"
    return page_url


def Get_Product_Name(item):
    product_name = item.find('div', {'class': '_4rR01T'})
    try:
        return product_name.text
    except AttributeError:
        print("No name")


def Get_Product_Actual_Price(item):
    product_price_actual = item.find('div', {'class': '_3I9_wc _27UcVY'})
    try:
        return product_price_actual.text
    except AttributeError:
        print("No actual")
        return '0'


def Get_Product_Discounted_Price(item):
    product_price_discounted = item.find('div', {'class': '_30jeq3 _1_WHN1'})
    try:
        return product_price_discounted.text
    except AttributeError:
        print("No discounted")
        return '0'


def Get_Product_Specifications(item):
    product_info = item.find_all('li', {'class': 'rgWa7D'})
    return_list = []
    try:
        for x in range(len(product_info)):
            return_list.append(product_info[x].text)
        return return_list
    except AttributeError:
        print("no info")
        return 'No info'


def Write_To_CSV(device_name, device_price_actual, device_price_discounted, device_info):
    temp_list = []
    if os.path.isfile('Flipkart.csv'):
        with open("Flipkart.csv", 'a', newline='', encoding='utf-8') as file_append:
            writer = csv.writer(file_append)
            line = ''
            for i in range(len(device_name)):
                temp_list.append(device_name[i])
                for individual in device_info[i]:
                    line += individual + '\015'
                temp_list.append(line)
                line = ''
                temp_list.append(device_price_discounted[i])
                temp_list.append(device_price_actual[i])
                writer.writerow(temp_list)
                temp_list = []

    else:
        with open("Flipkart.csv", 'w', newline='', encoding='utf-8') as file_write:
            writer = csv.writer(file_write)
            fields = ['Name', 'Info', 'Discounted', 'Actual']
            writer.writerow(fields)
            line = ''
            for i in range(len(device_name)):
                temp_list.append(device_name[i])
                for individual in device_info[i]:
                    line += individual + '\015'
                temp_list.append(line)
                line = ''
                temp_list.append(device_price_discounted[i])
                temp_list.append(device_price_actual[i])
                writer.writerow(temp_list)
                temp_list = []
