from selenium import webdriver
import time
from PIL import Image
import ddddocr
ocr = ddddocr.DdddOcr()


# 抠图
def matting():
    # 打开谷歌浏览器
    browser = webdriver.Chrome()
    # 打开网站首页
    browser.get("https://v3pro.houjiemeishi.com/PC/pages/login/login.html")
    # browser.get("http://192.168.139.129:8081/jpress/admin/login")
    # 网页最大化
    browser.maximize_window()
    # 登录页图片
    picture_name1 = 'login'+'.png'
    # 保存第一张截图
    browser.save_screenshot(picture_name1)
    # 定位元素
    ce = browser.find_element_by_id("captchaImg")
    # ce = browser.find_element_by_xpath('//*[@class="codeImg"]')
    # 打印元素位置、元素尺寸
    print(ce.location, ce.size)
    # 要抠验证码的图，先获取元素参数
    left = ce.location.get('x')
    top = ce.location.get('y')
    right = ce.size.get('width') + left
    height = ce.size.get('height') + top
    # 读取刚才截的第一张图
    im = Image.open(picture_name1)
    # 抠图
    img = im.crop((left, top, right, height))
    # 验证码块的图片
    picture_name2 = 'code'+'.png'
    # 保存图片
    img.save(picture_name2)
    time.sleep(5)
    browser.close()


# 通过 ddddocr 模块识别验证码
def ddocr(file):
    try:
        with open(file, 'rb') as f:
            img_bytes = f.read()
        res = ocr.classification(img_bytes)
        return res
    except:
        print("获取验证码失败，请继续！")


if __name__ == '__main__':
    print("抠图")
    matting()
    print("识别")
    code = ddocr('code.png')
    print(code)