# Mini_project01_crawling

In this project, you will learn how to use Selenium (Python) to control a WebDriver.
You are asked to implement mini_project_1.py using selenium_demo.py as a reference.

# Your tasks

### CDS Shop: http://10.113.178.219
- The account is {student_id_7_dgits_lower_case}@um.edu.mo
- The default password is {student_id_7_dgits_lower_case} (please change it when you first time login to the CDS shop)

## (1) Place the order (40%)
Your task is to make an order to a specific item (e.g. IPHONE 11 PRO 256GB MEMORY) on the system using your own account. Your script should be able to complete the following tasks automatically. 
1. Login from the first pages;
2. Go to the specific item page;
3. Add the item into your cart;
4. Proceed the checkout;
5. Fill the necessary information;
6. Place the order;
7. hack the Captcha.

### Instructions for hacking the Captcha can be found at the accompanying link:
- https://stackoverflow.com/questions/923885/capture-html-canvas-as-gif-jpg-png-pdf
- https://github.com/sml2h3/ddddocr

## (2) Find the top-x most expensive products for a given keyword (40%)
Your task is to collect the price of all products (of all pages) and return the top-x(e.g. 3) most expensive products as a list of dictionary and save it into csv format. The result contains the proudct name, price and description in descending order. 

e.g.:
```
product_name,product_price,description
"APPLE PENCIL(2ND GENERATION)",296.99,"Compatible with iPad mini(6th generation),..."
"APPLE MACBOOK AIR 11 INCHES",269,"Includes: 1-Pack MacBook Air 11 inches MD223LL/A..."
"APPLE WATCH SERIES 5",249.99,"GPS;Always-On Retina display;30% larger screen;Swim..."
```

## (3) Place your orders on the top-x products in task-2 (15%)

Your task is to make the orders to the top-5 expensive products on the system using your own account.


## (4) TBA
___
**Hints**

- Please change the password of your account;
- **Optimize** your code, e.g., try to replace the sleep function by [wait until](https://www.selenium.dev/documentation/webdriver/waits/);
- Learn how to use **headless selenium** to shorten the ordering time;
- You should first test your order script on those unlimited items;
<!-- - Nov 1 is a good day to test your script as the item quota is sufficient for everyone; -->
- You could consider to write a **monitoring script** to catch the limited item. However, your monitoring script should be designed in a polite manner.

