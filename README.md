# Mini_project01_crawling

In this project, you will learn how to use Selenium (Python) to interactive with the web (by [WebDriver](https://chromedriver.chromium.org/downloads)).
# Your tasks

### CDS Shop: http://10.113.178.219
- The account is {student_id_7_dgits_lower_case}@um.edu.mo
- The default password is {student_id_7_dgits_lower_case} (please change it when you first time login to the CDS shop)

## (1) Place the order (40%)

Your task is to make an order to a specific item (IPHONE 11 PRO 256GB MEMORY) on the system using your own account. Your script should be able to complete the following tasks automatically. 
1. Login from the first pages;
2. Go to the specific item page;
3. Add the item into your cart;
4. Proceed the checkout;
5. Fill the necessary information;
6. Place the order.

## (2) Find the top-5 most expensive products (40%)

Your task is to collect the price of all products (of all pages) and return the top-5 most expensive products as a list of dictionary and save it to json file. The return result contains the proudct name and price in descending order. 

```
[
    {
        "name": "CANNON EOS 80D DSLR CAMERA",
        "price": 929.99
    },
    {
        "name": "IPHONE 11 PRO 256GB MEMORY",
        "price": 599.99
    },
    {
        "name": "AIRPODS WIRELESS BLUETOOTH HEADPHONES",
        "price": 89.99
    }
]
```

## (3) Place your orders on the top-5 products in task-2 (15%)

Your task is to make the orders to the top-5 expensive products on the system using your own account.

## (4) Place the order to the limited items (15%)

In the last part of Project 01, we will simulate a competitive environment (first-come first-serve manner) that allows you to place orders to items of limited quotas. 

We will release our limited items (of a specific quota) on **specific dates** TBA and **specific time interval** TBA. 
- The name of the limited items will be released later;
- The limit item will appear on the CDS Shop at a random timestamp in that interval; 
- Everyone only allows to place one order per limited item. 
- During the competition, the TA will montior the system and help to remove those wrongly placed order at the back-end management system. 
- If we suspect any bad behavior from your codes (e.g., placing 200 orders at once), we may **ban your account** for the next few days;

**Quota for different days and mark distribution**

<!-- - Nov 1 Quota: 200 (1%) Name of the limited item: **GeForce RTX 4090 Liquid Cooling**
- Nov 3 Quota: 150 (2%) Name of the limited item: **Figure Anya Forger A Prize**
- Nov 5 Quota: 100 (3%) Name of the limited item: **SpaceX Extends Satellite Internet To RVs**
- Nov 6 Quota: 50  (4%) Name of the limited item: **SAO Nerve Gear and Registration Key**
- Nov 7 Quota: 10  (5%) Name of the limited item: **Pak The Merge** -->

The mark is given based on the purchase record of **your account**.

**Hints**

- Please change the password of your account;
- **Optimize** your code, e.g., try to replace the sleep function by wait until;
- Learn how to use **headless selenium** to shorten the ordering time;
- You should first test your order script on those unlimited items;
- Nov 1 is a good day to test your script as the item quota is sufficient for everyone;
- You could consider to write a **monitoring script** to catch the limited item. However, your monitoring script should be designed in a polite manner.

