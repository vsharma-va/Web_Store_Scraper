from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import os


def Create_Url(search_term):
    link = "https://www.reliancedigital.in/search?q={}:price-desc"
    f = search_term.replace(' ', '%20')
    url = link.format(f)
    url += '&page={}'
    return url


def Get_Product_Name(item):
    product_name = item.find('p', {'class': 'sp__name'})
    try:
        return product_name.text
    except AttributeError:
        print("No Name")


def Get_Product_Actual_Price(item):
    product_price_actual = item.find('em')
    try:
        return product_price_actual.text
    except AttributeError:
        print("No Actual Price")
        return '0'


def Get_Product_Discounted_Price(item):
    product_price_discounted = item.find('span', {'class': 'sc-bxivhb dmBTBc'})
    try:
        return product_price_discounted.text
    except AttributeError:
        print("No Discounted Price")
        return '0'


def Get_Product_Status(item):
    product_status = item.find_all('div', {'class': 'sc-hmzhuo eRHmmU'})
    try:
        return product_status[1].text
    except IndexError:
        return 'Available'


def Write_To_CSV(device_name, device_price_actual, device_price_discounted, device_specifications, device_info):
    temp_list = []
    if os.path.isfile('Reliance_Digital.csv'):
        with open("Reliance_Digital.csv", 'a', newline='', encoding='utf-8') as file_append:
            writer = csv.writer(file_append)
            line = ''
            for i in range(len(device_name)):
                temp_list.append(device_name[i])
                for individual in device_specifications[i]:
                    line += individual + '\015'
                temp_list.append(line)
                line = ''
                temp_list.append(device_price_discounted[i])
                temp_list.append(device_price_actual[i])
                temp_list.append(device_info[i])
                writer.writerow(temp_list)
                temp_list = []
        file_append.close()
    else:
        with open("Reliance_Digital.csv", 'w', newline='', encoding='utf-8') as file_write:
            writer = csv.writer(file_write)
            fields = ['Name', 'Specifications', 'Discounted', 'Actual', 'Status']
            writer.writerow(fields)
            line = ''
            for i in range(len(device_name)):
                temp_list.append(device_name[i])
                for individual in device_specifications[i]:
                    line += individual + '\015'
                temp_list.append(line)
                line = ''
                temp_list.append(device_price_discounted[i])
                temp_list.append(device_price_actual[i])
                temp_list.append(device_info[i])
                writer.writerow(temp_list)
                temp_list = []
        file_write.close()


def Sort_CSV():
    checked = []
    formatted = []
    data = []
    with open("Reliance_Digital.csv", 'r', encoding='utf-8') as file_read:
        reader = csv.reader(file_read)
        next(reader)
        for line in reader:
            data.append(line)
        for i in range(len(data)):
            file_read.seek(0)
            next(reader)
            record = data[i]
            to_check = record[0].split('(')
            if record not in formatted:
                formatted.append(record)
            checked.append(record)
            for line in reader:
                if to_check[0] == line[0].split('(')[0] and line not in checked and line not in formatted:
                    formatted.append(line)

    with open("Reliance_Digital_Sorted.csv", 'w', newline='', encoding='utf-8') as file_write:
        writer = csv.writer(file_write)
        fields = ['Name', 'Specifications', 'Discounted', 'Actual', 'Status']
        writer.writerow(fields)
        for li in formatted:
            writer.writerow(li)