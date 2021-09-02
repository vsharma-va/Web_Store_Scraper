import WebStoreScraper.Flipkart.Flipkart_Functions as Flipkart_Functions
from bs4 import BeautifulSoup
from selenium import webdriver


def main():
    driver = webdriver.Firefox(executable_path="../Resources/geckodriver.exe")
    term_to_search = input("Enter the search term")
    max_pages = int(input("Enter the number of pages you want to search"))
    url = Flipkart_Functions.Create_Url(term_to_search)

    for page in range(1, max_pages+1):
        print(page)
        # time.sleep(random.randint(1, 3))
        driver.get(url.format(page))
        device_name = []
        device_price_actual = []
        device_price_discounted = []
        device_info = []
        device_status = []
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('a', {'target': '_blank'})
        total_results = soup.find('span', {'class': '_10Ermr'})
        total_results_list = total_results.text.split(' ')
        total_results_num = int(total_results_list[3]) - int(total_results_list[1]) + 1
        print(total_results_num)
        for i in range(total_results_num):
            item = results[i]
            product_info = Flipkart_Functions.Get_Product_Status(item)
            product_name = Flipkart_Functions.Get_Product_Name(item)
            product_price_actual = Flipkart_Functions.Get_Product_Actual_Price(item)
            product_price_discounted = Flipkart_Functions.Get_Product_Discounted_Price(item)
            product_specifications = Flipkart_Functions.Get_Product_Specifications(item)

            device_name.append(product_name)
            device_price_actual.append(product_price_actual)
            device_price_discounted.append(product_price_discounted)
            device_info.append(product_specifications)
            device_status.append(product_info)

        Flipkart_Functions.Write_To_CSV(device_name, device_price_actual, device_price_discounted, device_info, device_status)
        Flipkart_Functions.Sort_CSV()


if __name__ == '__main__':
    main()
    print("Finished")
