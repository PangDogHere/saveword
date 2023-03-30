from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
# 设置Chrome浏览器的选项，使用headless模式隐藏浏览器窗口
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
# 创建Chrome浏览器对象
browser = webdriver.Chrome(options=chrome_options)
# 循环读取每一页的信息
data = []
for page in range(1, 3):  # 读取前10页的信息
    # 设置请求的URL
    url = f'https://nanchong.anjuke.com/sale/shunqing/p{page}/'
    # 发送请求并获取网页内容
    browser.get(url)
    html = browser.page_source
    # 判断是否出现验证弹窗
    if 'class="modal-content"' in html:
        print('需要手动验证...')
        while input('验证完成后，请输入1继续：') != '1':
            pass
        print('验证完成，继续爬取数据...')
        browser.get(url)
        html = browser.page_source
    # 解析网页内容
    soup = BeautifulSoup(html, 'html.parser')
    # 获取所有房屋信息
    houses = soup.select('ul#houselist-mod-new li.list-item')
    for house in houses:
        # 获取小区名
        name = house.select_one('div.property-content-info.property-content-info-comm').contents[0].strip()
        # 获取地址
        address = house.select_one('div.property-content-info.property-content-info-comm').contents[2].strip()
        # 获取楼层高度
        floor = house.select_one('div.property-content-info').contents[3].strip()
        # 获取建造年限
        year = house.select_one('div.property-content-info').contents[4].strip()
        data.append([name, address, floor, year])
    time.sleep(1)  # 等待1秒
# 关闭浏览器对象
browser.quit()
# 将数据存储到CSV文件中
df = pd.DataFrame(data, columns=['小区名', '地址', '楼层高度', '建造年限'])
df.to_csv('zhufang.csv', index=False, encoding='utf-8-sig')