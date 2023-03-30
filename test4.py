from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
import time
# 创建Chrome浏览器对象
browser = webdriver.Chrome()
# 循环读取每一页的信息
data = []
for page in range(1, 3):  # 读取前10页的信息
    # 设置请求的URL
    url = f'https://nanchong.anjuke.com/sale/shunqing/p{page}/'
    # 发送请求并获取网页内容
    browser.get(url)
    html = browser.page_source
    # 判断是否出现验证弹窗
    if 'id="ISDCaptcha"' in html:
        print('需要进行验证码验证...')
        # 等待验证码弹窗出现
        time.sleep(5)
        # 获取验证码弹窗
        captcha = browser.find_element_by_id('ISDCaptcha')
        # 获取滑块元素
        slider = captcha.find_element_by_class_name('geetest_slider_button')
        # 获取滑块距离左侧的距离
        distance = slider.location['x']
        # 获取滑块的宽度
        width = slider.size['width']
        # 计算需要滑动的距离
        distance += width / 2
        # 模拟鼠标点击滑块并滑动
        actions = ActionChains(browser)
        actions.click_and_hold(slider).perform()
        actions.move_by_offset(distance, 0).perform()
        actions.release().perform()
        # 等待验证成功
        time.sleep(3)
        print('验证完成，继续爬取数据...')
        browser.get(url)
        html = browser.page_source
    # 解析网页内容
    soup = BeautifulSoup(html, 'html.parser')
    # 获取所有房屋信息
    houses = soup.select('section.list')
    for house in houses:
        if house.text != ' ':
            # 获取小区名
            name = house.select_one('div.property-content-info.property-content-info-comm').contents[0].text.strip()
            # 获取地址
            address = house.select_one('div.property-content-info.property-content-info-comm').contents[2].text.strip()
            # 获取楼层高度
            floor = house.select_one('div.property-content-info').contents[3].text.strip()
            # 获取建造年限
            year = house.select_one('div.property-content-info').contents[4].text.strip()
            data.append([name, address, floor, year])
    time.sleep(1)  # 等待1秒
# 关闭浏览器对象
browser.quit()
# 将数据存储到CSV文件中
df = pd.DataFrame(data, columns=['小区名', '地址', '楼层高度', '建造年限'])
df.to_csv('zhufang.csv', index=False, encoding='utf-8-sig')