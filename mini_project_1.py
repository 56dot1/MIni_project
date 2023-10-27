import base64
from PIL import Image
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import *
import time
import csv
import os
import ddddocr

ocr = ddddocr.DdddOcr()


def open_driver(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # for ignore warning and error
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(7)  # set a waiting time limit for the browser driver
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
    search_bar = driver.find_element(By.NAME, "q")  # the name of search bar is declare as "q"
    search_bar.clear()  # clear the search_bar's contents
    search_bar.send_keys(keyword)  # fill the keyword to the bar
    time.sleep(operate_delay)
    search_bar.send_keys(Keys.RETURN)  # press enter to get the search result
    time.sleep(operate_delay)


def save_the_result(produts):
    import json
    with open('first_page_desctiption.json', 'w') as f:
        json.dump(produts, f, indent=4)


# Task 1: place the order
# implement the following function and run
def t1_place_the_order(product_name: str):
    def login():
        time.sleep(operate_delay)
        login_button = driver.find_element(By.XPATH, '//*[@id="basic-navbar-nav"]/div/a[2]')
        login_button.click()
        time.sleep(operate_delay)
        # enter email and password
        email = driver.find_element(By.XPATH, '//*[@id="email"]')
        email.send_keys("mc36614@um.edu.mo")
        time.sleep(operate_delay)
        password = driver.find_element(By.XPATH, '//*[@id="password"]')
        password.send_keys("mc36614")
        time.sleep(operate_delay)
        sign_in_button = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/form/button')
        sign_in_button.click()

    def search_a_product(product_name: str):
        search_bar = driver.find_element(By.XPATH, '//*[@id="basic-navbar-nav"]/form/input')
        search_bar.send_keys(product_name)
        time.sleep(operate_delay)
        search_bar.send_keys(Keys.RETURN)  # press enter to get the search result
        time.sleep(operate_delay)

    def add_to_cart():

        """
        搜索返回结果有两种情况，一种是只有一个与keywords相关的产品，另一种是多个相关产品,两种情况下Xpath不同，
        因此可以分开讨论这一问题。但无论是单个还是多个，本代码只取第一个放入购物车并完成后续付款过程。
        //*[@id="root"]/main/div/div/div/div/div/a/div/strong

        //*[@id="root"]/main/div/div/div[1]/div/div/a/div/strong

        //*[@id="root"]/main/div/div/div[2]/div/div/a/div/strong

        //*[@id="root"]/main/div/div/div[3]/div/div/a/div/strong

        //*[@id="canv"]

        注：后期似乎通过添加同类产品完善了这一问题，统一归为第二种情况处理
        但考虑到健壮性，仍保留此处更改
        """
        try:
            product_show = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/div/a/div/strong')
        except:
            product_show = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[1]/div/div/a/div/strong')

        product_show.click()
        time.sleep(operate_delay)
        # 加入购物车前进行判断，是否有货
        status = driver.find_element(By.XPATH,
                                     '//*[@id="root"]/main/div/div[1]/div[3]/div/div/div[2]/div/div[2]')

        add_cart = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div[1]/div[3]/div/div/div[4]/button')
        time.sleep(operate_delay)
        if status.text == 'In Stock':
            add_cart.click()
            time.sleep(operate_delay)
            checkout_button = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/div/div/div[2]/button')
            checkout_button.click()
        else:
            print("Product sold out choose another keyword!!!")
            back_home = driver.find_element(By.XPATH, '//*[@id="root"]/header/nav/div/a')
            back_home.click()


    def place_order():
        address = driver.find_element(By.XPATH, '//*[@id="address"]')
        time.sleep(operate_delay)
        address.send_keys("University of Macau,Graduate Student Dormitory, South Block 2")
        city = driver.find_element(By.XPATH, '//*[@id="city"]')
        time.sleep(operate_delay)
        city.send_keys("Macau")
        postal_code = driver.find_element(By.XPATH, '//*[@id="postalCode"]')
        time.sleep(operate_delay)
        postal_code.send_keys("999078")
        country = driver.find_element(By.XPATH, '//*[@id="country"]')
        time.sleep(operate_delay)
        country.send_keys("China")
        time.sleep(operate_delay)
        submit = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/form/button')
        submit.click()
        time.sleep(operate_delay)
        continue_button = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/form/button')
        continue_button.click()

        pay_button = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div[2]/div[2]/div/div/div[7]/button')
        pay_button.click()
        time.sleep(4)

    def hack_captcha():
        """
        针对验证码的获取方式，同样提供两种方式:定位后截图提取、直接canvas转png识别
        由于网页canvas定位有问题，故此处采取直接将canvas转为png后进行ocr识别，但先前使用的
        定位截图代码以备注的形式给出:
        
        captcha = driver.find_element(By.XPATH,'//*[@id="canv"]')
        print(captcha.location,captcha.size)
        # 获取相关的元素参数
        left = captcha.location # 1295
        top = captcha.size # 595
        right = captcha.size.get('width')+left
        height = captcha.size.get('height') + top
        
        im = Image.open(picture)
        # 抠图
        img = im.crop((left,top,right,height))

        captcha_img = 'captcha'+'.png'
        img.save(captcha_img)
        """
        time.sleep(2)
        captcha = driver.find_element(By.XPATH, '//*[@id="canv"]')
        canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);",
                                              captcha)

        captcha_data = base64.b64decode(canvas_base64)
        captcha_image = Image.open(io.BytesIO(captcha_data))
        captcha_image.save("captcha.png")
        time.sleep(operate_delay)
        # ddddocr 验证码识别：
        try:
            with open('captcha.png', 'rb') as f:
                img_bytes = f.read()
            res = ocr.classification(img_bytes)
            num = res
        except:
            print("Captcha Recognition Failure!!!")
        # 输入验证码
        input_bar = driver.find_element(By.XPATH, '//*[@id="user_captcha_input"]')
        input_bar.send_keys(num)
        time.sleep(operate_delay)
        subb_button = driver.find_element(By.XPATH,
                                          '//*[@id="root"]/main/div/div/div[2]/div/div/div[6]/div/div/div/div[3]/div/button')
        subb_button.click()
        time.sleep(operate_delay)
        # 如果验证失败，使用try except进行重新验证，点击提示框验证码会自动刷新
        try:
            # 尝试切换到提示框
            alert = driver.switch_to.alert
            alert.accept()
            hack_captcha()
        except NoAlertPresentException:
            # 如果没有提示框，点击左上角CDS SHOP返回主页
            print("Captcha Recognition is completed, the purchase is successful,will return to the main page soon")
            time.sleep(operate_delay)
            back_home = driver.find_element(By.XPATH, '//*[@id="root"]/header/nav/div/a')
            back_home.click()

    login()
    search_a_product(product_name)
    add_to_cart()
    place_order()
    hack_captcha()


# Task 2: Find the top-x for a given keyword
def t2_find_top_x(x, keyword):
    top_x_result = []

    search_a_keyword(keyword)
    # 搜索完成后获取共有多少页面
    page_items = driver.find_elements(By.CLASS_NAME, 'page-item')
    page_num = 0
    for page in page_items:
        page_num += 1
    # 用于后续判断翻页结束位置
    exit_code = 1

    # Please note that the price is a floating number
    def get_all_product_price_in_one_page():
        try:
            time.sleep(2)
            items_all = wait.until(presence_of_all_elements_located((By.CLASS_NAME, "card-body")))

            for item in items_all:
                link_of_product = item.find_element(By.TAG_NAME, 'a')
                # 根据系统
                if os.name == 'posix':
                    link_of_product.send_keys(Keys.COMMAND, Keys.RETURN)
                else:
                    link_of_product.send_keys(Keys.CONTROL, Keys.RETURN)

                windows = driver.window_handles
                driver.switch_to.window(windows[-1])

                ls_items = wait.until(presence_of_all_elements_located((By.CLASS_NAME, 'list-group-item')))
                status = driver.find_element(By.XPATH,
                                             '//*[@id="root"]/main/div/div[1]/div[3]/div/div/div[2]/div/div[2]')
                product_url = driver.current_url
                time.sleep(operate_delay)

                product = {}
                name = ls_items[0].text
                price = ls_items[2].text
                description = ls_items[3].text
                product['name'] = name
                product['price'] = price
                product['description'] = description
                product['status'] = status.text
                product['url'] = product_url
                products.append(product)
                print(product, end='\n\n')
                driver.close()
                time.sleep(operate_delay)
                driver.switch_to.window(windows[0])
        except Exception as e:
            print("Cannot find data")
            nonlocal exit_code
            exit_code = 0

    def go_to_next_page():
        """
        通过控制href进行换页操作
        """
        try:
            current_url = driver.current_url

            # 检查当前URL是否包含/page/，如果不包含，将/page/1添加到URL中
            if '/page/' not in current_url:
                current_url += '/page/1'

            # 提取当前页数
            page_number = int(re.search(r'/page/(\d+)', current_url).group(1))

            # 构建下一页的URL
            next_page_number = page_number + 1
            next_page_url = re.sub(r'/page/\d+', f'/page/{next_page_number}', current_url)

            driver.get(next_page_url)
            return True
        except Exception as e:
            print("cannot find next page ")
            return False

    def save_dict_to_csv():
        # 根据价格进行排序
        sorted_products = sorted(products, key=lambda product: float(product['price'].split('$')[1]), reverse=True)
        top_x_products = sorted_products[:x]
        # 保存为csv文件
        with open('top_%d_result_of_%s.csv' % (x, keyword), 'w') as f:
            fieldnames = ['name', 'price', 'description']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for things in top_x_products:
                things_data = {key: things[key] for key in fieldnames}
                writer.writerow(things_data)
        print("CSV file has been saved")
        return sorted_products

    next_num = 1
    while exit_code:
        get_all_product_price_in_one_page()
        time.sleep(operate_delay)
        if next_num != page_num:
            go_to_next_page()
            next_num += 1
        else:
            break

    a = save_dict_to_csv()
    return a


# Task 3: Place the order to the top-5 products you found in task-2
def t3_order_top5(x, keywords):
    """
    task3 开始前，先对task2中的代码进行微调，补充商品状态和商品链接，前者用来确定是否可以购买
    后者则是用来取巧加入购物车
    通过检查监测后台网络变化，点击加入购物车时会发送一段内容，经测试后发现，只需要键入以下链接即可加入购物车
    http://10.113.178.219/cart/652d15a43be4ad118888bfa2?qty=1
    http://10.113.178.219/cart/652d15a43be4ad118888bfa4?qty=1
    因此，加入购物车过程为，替换掉商品编号之后，输入对应的链接，统计完要购买的商品数量后输入次数

    购买牵涉的问题，商品是否有货？返回的商品够不够五个？
    问题1由status解决
    问题2小于等于五个全买，大于五个买前五个，

    """

    def login():
        time.sleep(operate_delay)
        login_button = driver.find_element(By.XPATH, '//*[@id="basic-navbar-nav"]/div/a[2]')
        login_button.click()
        time.sleep(operate_delay)
        # enter email and password
        email = driver.find_element(By.XPATH, '//*[@id="email"]')
        email.send_keys("mc36614@um.edu.mo")
        time.sleep(operate_delay)
        password = driver.find_element(By.XPATH, '//*[@id="password"]')
        password.send_keys("mc36614")
        time.sleep(operate_delay)
        sign_in_button = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/form/button')
        sign_in_button.click()

    def place_order():
        address = driver.find_element(By.XPATH, '//*[@id="address"]')
        time.sleep(operate_delay)
        address.send_keys("University of Macau,Graduate Student Dormitory, South Block 2")
        city = driver.find_element(By.XPATH, '//*[@id="city"]')
        time.sleep(operate_delay)
        city.send_keys("Macau")
        postal_code = driver.find_element(By.XPATH, '//*[@id="postalCode"]')
        time.sleep(operate_delay)
        postal_code.send_keys("999078")
        country = driver.find_element(By.XPATH, '//*[@id="country"]')
        time.sleep(operate_delay)
        country.send_keys("China")
        time.sleep(operate_delay)
        submit = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/form/button')
        submit.click()
        time.sleep(operate_delay)
        continue_button = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/form/button')
        continue_button.click()

        pay_button = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div[2]/div[2]/div/div/div[7]/button')
        pay_button.click()
        time.sleep(4)

    def hack_captcha():

        time.sleep(2)
        captcha = driver.find_element(By.XPATH, '//*[@id="canv"]')
        canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);",
                                              captcha)

        captcha_data = base64.b64decode(canvas_base64)
        captcha_image = Image.open(io.BytesIO(captcha_data))
        captcha_image.save("captcha.png")
        time.sleep(operate_delay)
        # ddddocr 验证码识别：
        try:
            with open('captcha.png', 'rb') as f:
                img_bytes = f.read()
            res = ocr.classification(img_bytes)
            num = res
        except:
            print("Captcha Recognition Failure!!!")
        # 输入验证码
        input_bar = driver.find_element(By.XPATH, '//*[@id="user_captcha_input"]')
        input_bar.send_keys(num)
        time.sleep(operate_delay)
        subb_button = driver.find_element(By.XPATH,
                                          '//*[@id="root"]/main/div/div/div[2]/div/div/div[6]/div/div/div/div[3]/div/button')
        subb_button.click()
        time.sleep(operate_delay)
        # 如果验证失败，使用try except进行重新验证，点击提示框验证码会自动刷新
        try:
            # 尝试切换到提示框
            alert = driver.switch_to.alert
            alert.accept()
            hack_captcha()
        except NoAlertPresentException:
            # 如果没有提示框，点击左上角CDS SHOP返回主页
            print("Captcha Recognition is completed, the purchase is successful,will return to the main page soon")
            time.sleep(operate_delay)
            back_home = driver.find_element(By.XPATH, '//*[@id="root"]/header/nav/div/a')
            back_home.click()

    login()
    time.sleep(operate_delay)
    top_x_result = t2_find_top_x(x, keywords)
    # 首先需要判断搜索结果够不够五个
    results_num = len(top_x_result)
    print(results_num)
    if results_num <= 5:
        # 小于等于五个直接全买
        for goods in top_x_result:
            if goods['status'] == 'In Stock':
                url_goods = goods['url'].split("/")
                goods_id = url_goods[-1]
                cart_url = f"http://10.113.178.219/cart/{goods_id}?qty=1"
                time.sleep(operate_delay)
                driver.get(cart_url)
            else:
                continue
            time.sleep(2)
    else:
        # 大于五个买前五个，加个计数的进行判断
        control_code = 0
        for goods in top_x_result:
            if control_code < 5:
                if goods['status'] == 'In Stock':
                    url_goods = goods['url'].split("/")
                    goods_id = url_goods[-1]
                    cart_url = f"http://10.113.178.219/cart/{goods_id}?qty=1"
                    time.sleep(operate_delay)
                    driver.get(cart_url)
                else:
                    continue
            control_code += 1

    time.sleep(operate_delay)
    checkout_button = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/div/div/div[2]/button')
    checkout_button.click()
    place_order()
    hack_captcha()


# 代码执行

# keywords输入
t1_keyword = input("please input t1's keyword:")
t2_keyword = input("please input t2's keyword:")
while True:
    try:
        user_input = input("please input t2's top products number:")
        t2_top_num = int(user_input)  # 尝试将输入转换为浮点数
        break  # 退出循环
    except ValueError:
        print("WRONG: please in put number")

url = 'http://10.113.178.219'  # the url of shopping cart
operate_delay = 1  # the time gap between each process
products = []
# end of parameters declaration
driver = open_driver(url)
wait = WebDriverWait(driver, 10)

# 任务执行
# 其中t3用的是t2的参数，如有需要可进行更改
t1_place_the_order(t1_keyword)
t2_find_top_x(t2_top_num, t2_keyword)
t3_order_top5(t2_top_num, t2_keyword)

# for task in [t1_place_the_order, t2_find_top_x, t3_order_top5]:
#     driver = open_driver(url)
#     wait = WebDriverWait(driver, 10)  # set a maximum implicit waiting time for the browser driver
#     if task == t1_place_the_order:
#         task('IPHONE 11 PRO 256GB MEMORY')
#     elif task == t2_find_top_x:
#         task(3, 'apple')
#     else:
#         task()
#     driver.close()
