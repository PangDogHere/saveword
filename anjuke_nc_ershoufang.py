from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
# 创建Chrome浏览器对象
browser = webdriver.Chrome()
# 设置要爬取的页面URL
urls = [
    'https://nanchong.anjuke.com/sale/shunqing/',
    'https://nanchong.anjuke.com/sale/nanbu/',
    'https://nanchong.anjuke.com/sale/gaopingb/',
    'https://nanchong.anjuke.com/sale/jialing/',
    'https://nanchong.anjuke.com/sale/zhong/',
    'https://nanchong.anjuke.com/sale/yingshanab/',
    'https://nanchong.anjuke.com/sale/xichong/',
    'https://nanchong.anjuke.com/sale/pengan/',
    'https://nanchong.anjuke.com/sale/yilong/'
]
# 循环读取每个页面的信息
data = []
for url in urls:    
    while True:
        # 访问第一页
        browser.get(url)
        # 解析网页内容
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # 获取所有房屋信息
        houses = soup.select('.property')
        for house in houses:
            if house.select_one('div.property-content-info.property-content-info-comm') is not None:
                # 获取小区名
                name = house.select_one('div.property-content-info.property-content-info-comm').contents[0].text.strip()
                # 获取地址
                address = house.select_one('div.property-content-info.property-content-info-comm').contents[2].text.strip()
                # 获取楼层高度
                floor = house.select_one('div.property-content-info').contents[6].text.strip()
                # 获取建造年限
                year = house.select_one('div.property-content-info').contents[8].text.strip()
                data.append([name, address, floor, year])
        # 查找下一页按钮
        next_page = soup.select_one('.next.click-forbid')
        if next_page is not None :
            # 没有找到下一页按钮或者已经到达最后一页，退出循环
            break
        next_page = soup.select_one('.next.next-active')
        if next_page is not None:
            # 点击下一页按钮
            url = next_page['href']
            # 等待一段时间
        time.sleep(1)
# 关闭浏览器对象
browser.quit()
# 将数据存储到CSV文件中
df = pd.DataFrame(data, columns=['小区名', '地址', '楼层高度', '建造年限'])
df.to_csv('nanchong_ershoufang.csv', index=False, encoding='utf-8-sig')
print("完成")