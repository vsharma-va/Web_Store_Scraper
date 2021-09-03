# import WebStoreScraper.Reliance_Digital.Reliance_Digital as Reliance
# import WebStoreScraper.Amazon.Amazon as Amazon
# import WebStoreScraper.Flipkart.Flipkart as Flipkart
import pandas as pd


def Get_Amazon():
    data = pd.read_csv("data/Amazon_Sorted.csv")
    return_dict = {}
    product_name = data['Name']
    product_price_discounted = data['Discounted']
    product_price_actual = data['Actual']
    for i in range(len(data)):
        split = product_name[i].split('(')
        required_name = str(split[0])
        colour = str(split[1].split(',')[0])
        dict_key = required_name + ' ' + colour
        if product_price_discounted[i] == '0' and product_price_actual[i] == '0':
            return_dict[dict_key] = '0'
        elif product_price_actual[i] == '0':
            return_dict[dict_key] = product_price_discounted[i]
        elif product_price_discounted[i] == '0':
            return_dict[dict_key] = product_price_actual[i]
        elif product_price_discounted[i] != '0' and product_price_discounted[i] != '0':
            return_dict[dict_key] = product_price_discounted[i]
    return return_dict


def Get_Flipkart():
    data = pd.read_csv("data/Flipkart_Sorted.csv")
    return_dict = {}
    product_name = data['Name']
    product_price_discounted = data['Discounted']
    product_price_actual = data['Actual']
    for i in range(len(data)):
        split = product_name[i].split('(')
        required_name = str(split[0])
        colour = str(split[1].split(',')[0])
        dict_key = required_name + ' ' + colour
        if product_price_discounted[i] == '0' and product_price_actual[i] == '0':
            return_dict[dict_key] = '0'
        elif product_price_actual[i] == '0':
            return_dict[dict_key] = product_price_discounted[i]
        elif product_price_discounted[i] == '0':
            return_dict[dict_key] = product_price_actual[i]
        elif product_price_discounted[i] != '0' and product_price_discounted[i] != '0':
            return_dict[dict_key] = product_price_discounted[i]
    return return_dict


def Get_Reliance_Digital():
    data = pd.read_csv("data/Reliance_Digital_Sorted.csv")
    return_dict = {}
    product_name = data['Name']
    product_price_discounted = data['Discounted']
    product_price_actual = data['Actual']
    for i in range(len(data)):
        split = product_name[i].split(',')  # 0 = name, 1 = ram, 2 = colour, 3 = category
        name_split = split[0].split(' ')
        required_name_list = (name_split[0:len(name_split) - 2])
        required_name = ' '.join(required_name_list)
        colour = str(split[2])
        dict_key = required_name + ' ' + colour
        if product_price_discounted[i] == '0' and product_price_actual[i] == '0':
            return_dict[dict_key] = '0'
        elif product_price_actual[i] == '0':
            return_dict[dict_key] = product_price_discounted[i]
        elif product_price_discounted[i] == '0':
            return_dict[dict_key] = product_price_actual[i]
        elif product_price_discounted[i] != '0' and product_price_discounted[i] != '0':
            return_dict[dict_key] = product_price_discounted[i]
    return return_dict


def main():
    x = Get_Amazon()
    y = Get_Flipkart()
    z = Get_Reliance_Digital()

main()
