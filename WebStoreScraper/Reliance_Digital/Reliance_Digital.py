import selenium.common.exceptions
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import WebStoreScraper.Reliance_Digital.Reliance_Digital_Functions as Reliance_Digital_Functions

options = webdriver.FirefoxOptions()
options.set_preference("dom.push.enabled", False)
driver = webdriver.Firefox(options=options, executable_path='../Resources/geckodriver.exe')
driver.maximize_window()


def Get_All_Categories():
    filter_list = []
    time.sleep(2)
    see = driver.find_element_by_xpath("//div[@class='show-more__action']")
    see.click()
    categories = driver.find_elements_by_xpath("//div[@class='sf sf__accord__locked']")
    for i in categories:
        filter_list.append(i.text)
    category_list = []
    for elements in filter_list:
        if 'Category' in elements:
            category_list.append(elements.split('\n'))

    category_list[0].remove('Category')
    category_list[0].remove('See less')
    return category_list  # list of list


def Go_To_User_Defined_Category(index_number, category_list):
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
        (By.XPATH, "//div[@class='sp__product']")))
    time.sleep(2)
    selected_category = category_list[0][index_number]
    xpath = "//input[@id='category-{}']"
    xpath_full = xpath.format(selected_category)
    l = driver.find_element_by_xpath(xpath_full)
    l.send_keys(Keys.SPACE)
    time.sleep(10)


def Get_Product_Specifications(product_name, i):
    info_value_list = []
    # click on item to open its page
    link = driver.find_elements_by_xpath("//p[@class='sp__name']")
    link[i].click()
    new_window = driver.window_handles[1]
    original_window = driver.window_handles[0]
    driver.switch_to.window(new_window)
    # click on see more
    WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((
       By.XPATH, "//div[@class='pdp__tab-info__list__name blk__sm__6 blk__xs__6']")))
    try:
        time.sleep(1)
        see_more = driver.find_element_by_xpath("//span[@id='specificationsIdMain']")
        driver.execute_script("arguments[0].scrollIntoView();", see_more)
        driver.execute_script("arguments[0].click()", see_more)
    except selenium.common.exceptions.StaleElementReferenceException:
        print('except')
        see_more = driver.find_element_by_xpath("//div[@id='RIL_HeaderSpecification']")
        see_more.click()
    info_soup = BeautifulSoup(driver.page_source, 'html.parser')
    info_value = info_soup.find_all('div', {'class': 'pdp__tab-info__list__value blk__sm__6 blk__xs__6'})
    for k in info_value:
        info_value_list.append(k.text)
    index_remove = []
    for i in range(len(info_value_list) - 1):
        if product_name.find(info_value_list[i]) != -1:
            index_remove.append(i)
        if info_value_list[i].find('cms') != -1:
            index_remove.append(i)
        if info_value_list[i].find('Email id') != -1:
            index_remove.append(i)
        if info_value_list[i].find('Yes') != -1:
            index_remove.append(i)
        if info_value_list[i].find('Reliance') != -1:
            index_remove.append(i)
    y = 0
    for h in index_remove:
        info_value_list.pop(h - y)
        y += 1
    driver.close()
    driver.switch_to.window(original_window)
    return info_value_list


def main():
    term_to_search = input("Enter the search term")
    max_pages = int(input("Enter the number of pages you want to search"))
    url = Reliance_Digital_Functions.Create_Url(term_to_search)
    for page in range(1, max_pages+1):
        print(page)
        display_counter = 0
        category_list = []
        # time.sleep(random.randint(1, 3))
        driver.get(url.format(page))
        device_name = []
        device_price_actual = []
        device_price_discounted = []
        device_info = []
        device_specifications = []
        category_list = Get_All_Categories()
        if page == 1:
            for k in category_list:
                for category_element in k:
                    print(display_counter, category_element)
                    display_counter += 1
            user_input = int(input("Enter the index number of the category you want to search"))
            Go_To_User_Defined_Category(user_input, category_list)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('a', {'target': '_blank'})
        for i in range(len(results)):
            item = results[i]
            product_info = Reliance_Digital_Functions.Get_Product_Status(item)
            product_name = Reliance_Digital_Functions.Get_Product_Name(item)
            product_price_actual = Reliance_Digital_Functions.Get_Product_Actual_Price(item)
            product_price_discounted = Reliance_Digital_Functions.Get_Product_Discounted_Price(item)
            product_specifications = Get_Product_Specifications(product_name, i)

            device_name.append(product_name)
            device_price_actual.append(product_price_actual)
            device_price_discounted.append(product_price_discounted)
            device_info.append(product_info)
            device_specifications.append(product_specifications)

        Reliance_Digital_Functions.Write_To_CSV(device_name, device_price_actual, device_price_discounted,
                                                device_specifications, device_info)
        Reliance_Digital_Functions.Sort_CSV()


if __name__ == '__main__':
    main()
    print("Finished")