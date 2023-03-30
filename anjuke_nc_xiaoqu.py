from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
# 创建Chrome浏览器对象
browser = webdriver.Chrome()
# 设置要爬取的页面URL
urls = [
    'https://nanchong.anjuke.com/community/shunqing/',
    'https://nanchong.anjuke.com/community/nanbu/',
    'https://nanchong.anjuke.com/community/gaopingb/',
    'https://nanchong.anjuke.com/community/jialing/',
    'https://nanchong.anjuke.com/community/zhong/',
    'https://nanchong.anjuke.com/community/yingshanab/',
    'https://nanchong.anjuke.com/community/xichong/',
    'https://nanchong.anjuke.com/community/pengan/',
    'https://nanchong.anjuke.com/community/yilong/'
]
# 循环读取每个页面的信息
data = []
for url in urls:    
    while True:
        # 随机等待一段时间
        random_time = random.randint(1800, 2800)
        # 访问第一页
        browser.get(url)
        # 解析网页内容
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # 获取所有房屋信息
        houses = soup.select('div.li-info')
        for house in houses:
            if house.select_one('div.li-title') is not None:
                # 获取小区名
                if house.select_one('.li-title') is not None:
                    name = house.select_one('.li-title').contents[0].text.strip()
                else:
                    name = "无"
                # 获取地址
                if house.select_one('.props.nowrap') is not None:
                    address = house.select_one('.props.nowrap').contents[2].text.strip()
                else:
                    address ="无"
                # 获取楼层高度
                # floor = house.select_one('div.property-content-info').contents[6].text.strip()
                # 获取建造年限
                if house.select_one('.year') is not None:
                    year = house.select_one('.year').contents[0].text.strip()
                else:
                    year = "无"
                data.append([name, address, year]) #floor
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
        time.sleep(random_time / 1000)
# 关闭浏览器对象
browser.quit()
# 将数据存储到CSV文件中
df = pd.DataFrame(data, columns=['小区名', '地址', '建造年限'])
df.to_csv('nanchong_xiaoqu2.csv', index=False, encoding='utf-8-sig')
print("完成")