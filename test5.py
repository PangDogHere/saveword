from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
# 创建Chrome浏览器对象
browser = webdriver.Chrome()
# 循环读取每一页的信息
data = []
for page in range(1, 51):  # 读取前10页的信息
    # 设置请求的URL
    url = f'https://nanchong.anjuke.com/sale/shunqing/p{page}/'
    # 发送请求并获取网页内容
    browser.get(url)
    html = browser.page_source
    # 解析网页内容
    soup = BeautifulSoup(html, 'html.parser')
    # 获取所有房屋信息
    houses = soup.select('div.property')
    for house in houses:
        if house.select_one('div.property-content-info.property-content-info-comm') is not None:
            # 获取小区名
            name = house.select_one('div.property-content-info.property-content-info-comm').contents[0].text.strip()
            # 获取地址
            address = house.select_one('div.property-content-info.property-content-info-comm').contents[2].text.strip()
            # 获取楼层高度
            floor = house.select_one('div.property-content-info').contents[6].text.strip()
            # 获取建造年限
            year = house.select_one('div.property-content-info').contents[7].text.strip()
            data.append([name, address, floor, year])
    time.sleep(1)  # 等待1秒
# 关闭浏览器对象
browser.quit()
# 将数据存储到CSV文件中
df = pd.DataFrame(data, columns=['小区名', '地址', '楼层高度', '建造年限'])
df.to_csv('安居-顺庆-二手.csv', index=False, encoding='utf-8-sig')
print("完成")