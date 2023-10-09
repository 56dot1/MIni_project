from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import *
import time
import os

#---------------------------------------------------------------------------------------
# basic function for reference
def open_driver(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # for ignore warning and error
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(7) # set a waiting time limit for the browser driver
    driver.maximize_window()
    return driver

def search_a_keyword(keyword):
    '''
    find_element(By.name,'q') act equivalant to find_element_by_name('q')
    the method find_element_by_name is deprecated in latest version
    
    To search a keyword you need to fill in the keyword and press enter.
    We use send_keys() function to simulate keyborad inputs.
    ref:https://selenium-python.readthedocs.io/locating-elements.html#
    '''
    search_bar = driver.find_element(By.NAME,"q") # the name of search bar is declare as "q"
    search_bar.send_keys(keyword)  # fill the keyword to the bar
    time.sleep(operate_delay)
    search_bar.send_keys(Keys.RETURN) # press enter to get the search result
    time.sleep(operate_delay)

def save_the_result(produts):
    import json
    with open('first_page_desctiption.json','w') as f:
        json.dump(produts,f,indent=4)    


#---------------------------------------------------------------------------------------

# Task 1: place the order
# implement the following function and run
def t1_place_the_order(product_name:str):
    def login():
        pass
    def search_a_keyword(product_name:str):
        pass
    def add_to_cart():
        pass
    def place_order():
        pass
    def hack_captcha():
        pass
    login()
    search_a_keyword(product_name)
    add_to_cart()
    place_order()
    hack_captcha()


# Task 2: Find the top-x for a given keyword
def t2_find_top_x(x, keyword):
    top_x_result = []
    product = {'name':'','price':0}
    search_a_keyword(keyword)
    # Please note that the price is a floating number
    def get_all_product_price_in_one_page():
        pass
    def go_to_next_page():
        pass
    def save_dict_to_csv():
        with open('top_%d_result_of_%s.csv'%(x, keyword),'w') as f:
            pass
        pass
    while True:
        get_all_product_price_in_one_page()
        go_to_next_page()
        break
        #you should break the loop if next_page does not exist 
    save_dict_to_csv()
    return top_x_result


# Task 3: Place the order to the top-5 products you found in task-2
def t3_order_top5():
    top_x_result = t2_find_top_x()
    for product in top_x_result:
        t1_place_the_order(product)


url = 'http://10.113.178.219' # the url of shopping cart
operate_delay = 1 # the time gap between each process
# end of parameters declaration


for task in [t1_place_the_order,t2_find_top_x,t3_order_top5]:
    driver = open_driver(url) 
    wait = WebDriverWait(driver, 10) # set a maximum implicit waiting time for the browser driver
    if task == t1_place_the_order:
        task('IPHONE 11 PRO 256GB MEMORY')
    elif task == t2_find_top_x:
        task(3, 'apple')
    else:
        task()
    driver.close()
