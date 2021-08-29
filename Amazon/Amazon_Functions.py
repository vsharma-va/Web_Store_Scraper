import csv
import os


def Create_Url(search_item):
    template = "https://www.amazon.in/s?k={}&ref=nb_sb_noss_2&s=price-desc-rank"
    item = search_item.replace(' ', '+')
    url = template.format(item)
    url += "&page={}"           # this is what amazon adds to move to the next page
    return url


def Check_Amazons_Choice(item):
    amazons_choice = item.find('span', {'aria-label': "Amazon's Choice"})
    if amazons_choice is not None:
        return True
    elif amazons_choice is None:
        return False


def Check_Hovered_Sponsor(item):
    hovered_sponsor = item.find('span', {'class': 's-label-popover-hover'})
    if hovered_sponsor is not None:
        return True
    elif hovered_sponsor is None:
        return False


# finds out the price and discounted price of the item
def Return_Discount_Actual_Price(item):
    product_price = item.find('a', {'class': 'a-size-base a-link-normal a-text-normal'})
    return_list = []
    try:
        discounted_and_actual_wrong = product_price.text.split(' ', 1)
        unwanted_discounted = discounted_and_actual_wrong[0].split('₹')
        if len(unwanted_discounted) >= 2:
            discounted = unwanted_discounted[1]
        else:
            discounted = unwanted_discounted[0]

        unwanted_actual = discounted_and_actual_wrong[1].split('₹')
        if len(unwanted_actual) >= 2:
            actual = unwanted_actual[1]
        else:
            actual = unwanted_actual[0]
        return_list.append(discounted)
        return_list.append(actual)
    except AttributeError:
        return_list.append('0')
        return_list.append('0')
    return return_list


# deletes selected products
# it displays two groups of items with index next to them
def Delete_Amazon_Or_Hovered(hovered_items, hovered_price_discount, hovered_price_actual, amazons_items,
                             amazons_price_actual, amazons_price_discount):
    not_done = True
    while not_done:
        counter = 0
        print('\n\n')
        print("Hovered Sponsored Group->")
        for z in hovered_items:
            print(counter, z)
            counter += 1
        counter = 0
        print('\n\n')
        print("Amazons Choice Group->")
        for x in amazons_items:
            print(counter, x)
            counter += 1
        print('\n\n')
        selected_group = input('''Enter the first three letters of the group you want to delete from: 
Or Enter q to exit  ''')

        if selected_group == "q":
            not_done = False
            continue

        delete_item_idx = int(input('''Enter the index of the item you want to delete
Or Enter an negative number to exit  '''))
        if delete_item_idx < 0:
            not_done = False
            continue
        if selected_group == "hov" and delete_item_idx >= 0:
            hovered_items.pop(delete_item_idx)
            hovered_price_discount.pop(delete_item_idx)
            hovered_price_actual.pop(delete_item_idx)
        elif selected_group == "ama" and delete_item_idx >= 0:
            amazons_items.pop(delete_item_idx)
            amazons_price_actual.pop(delete_item_idx)
            amazons_price_discount.pop(delete_item_idx)

        else:
            print('\n\n')
            print("You may have selected a group which is not present")

    return [[hovered_items, hovered_price_actual, hovered_price_discount],
            [amazons_items, amazons_price_actual, amazons_price_discount]]


# adds all of the products together in device_names actual_price and discount_price lists
def Add_Amazon_Or_Hovered_Items(hovered_items, amazons_items, device_names, actual_price, discount_price,
                                amazons_price_discount,
                                amazons_price_actual, hovered_price_actual, hovered_price_discount):
    counter = 0
    print('\n\n')
    print("These are the remaining items. What would you like to do with them ?")
    for z in hovered_items:
        print(counter, z)
        counter += 1
    print('\n\n')
    for x in amazons_items:
        print(counter, x)
        counter += 1

    print('\n\n')
    print("Type ad to add all the remaining devices to the csv file if they are not already present")
    print("Type de to discard all the remaining devices")
    user_answer = input("Enter your choice")
    if user_answer == "ad":
        try:
            for i in range(len(hovered_items)):
                if hovered_items[i] not in device_names:
                    device_names.append(hovered_items[i])
                    actual_price.append(hovered_price_actual[i])
                    discount_price.append(hovered_price_discount[i])
        except IndexError:
            print("no records left in hovered_items")

        try:
            for h in range(len(amazons_items)):
                if amazons_items[h] not in device_names:
                    device_names.append(amazons_items[h])
                    actual_price.append(amazons_price_actual[h])
                    discount_price.append(amazons_price_discount[h])
        except IndexError:
            print("No records left in amazons_items")

    elif user_answer == "de":
        print("Discarded Successfully")

    return [device_names, actual_price, discount_price]


# just writes the three lists in a csv file
# if the file already exists it appends to it other wise it creates a new one
def Write_To_CSV(device_names, actual_price, discounted_price):
    temp_list = []
    if os.path.isfile('Amazon.csv'):
        with open("Amazon.csv", 'a', newline='', encoding="utf-8") as file_write:
            writer = csv.writer(file_write)
            for i in range(len(device_names)):
                temp_list.append(device_names[i])
                try:
                    temp_list.append(actual_price[i])
                except IndexError:
                    temp_list.append(0)

                try:
                    temp_list.append(discounted_price[i])
                except IndexError:
                    temp_list.append(0)
                    print("Index error in temp_list")
                writer.writerow(temp_list)
                temp_list = []
    else:
        fields = ['Name', 'Actual', 'Discounted']
        with open('Amazon.csv', 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(fields)
            for i in range(len(device_names)):
                temp_list.append(device_names[i])
                try:
                    temp_list.append(actual_price[i])
                except IndexError:
                    temp_list.append(0)

                try:
                    temp_list.append(discounted_price[i])
                except IndexError:
                    temp_list.append(0)
                    print("Index error in temp_list")
                writer.writerow(temp_list)
                temp_list = []
