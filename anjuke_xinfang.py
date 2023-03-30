from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
# 创建Chrome浏览器对象
browser = webdriver.Chrome()
# 设置要爬取的页面URL
urls = [
    'https://nan.fang.anjuke.com/loupan/all/'
]
# 循环读取每个页面的信息
data = []
for url in urls:    
    # url_Tmp 中转 URL
    url_Tmp = url
    while True:        
        # 随机等待一段时间
        random_time = random.randint(1800, 2800)
        # 访问第一页
        browser.get(url)
        # 解析网页内容
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # 获取所有房屋信息
        houses = soup.select('.key-list.imglazyload > div.item-mod')
        for house in houses:
            if house.select_one('.infos') is not None:
                # 获取小区名
                if house.select_one('.infos') is not None:
                    name = house.select_one('span.items-name').contents[0].text.strip()
                    address = house.select_one('span.list-map').contents[0].text.strip()
                else:
                    name = "无"
                    address = "无"
                # 获取地址
                # if house.select_one('.props.nowrap') is not None:
                #     address = house.select_one('.props.nowrap').contents[2].text.strip()
                # else:
                #     address ="无"
                # 获取楼层高度
                if  house.select_one('.houseInfo') is not None:
                    floor = house.select_one('.houseInfo').contents[1].text.strip()
                else:
                    floor = "无"
                # 获取建造年限
                # if house.select_one('.year') is not None:
                #     year = house.select_one('.year').contents[0].text.strip()
                # else:
                #     year = "无"
                data.append([name, address,floor]) #year
        # 查找下一页按钮
        # next_page = soup.select_one('.next-page.next-link')
        next_pagedisable = soup.select_one('.next-page.stat-disable')
        # if next_page.text.find('下一页') == -1:
        if next_pagedisable :
            # 没有找到下一页按钮或者已经到达最后一页，退出循环
            break
        else:
            #获得页码和总页码
            # page_data=json.loads(soup.select_one('.page-box.house-lst-page-box').attrs["page-data"])
            # curPage=json.loads(soup.select_one('.page-box.house-lst-page-box').attrs["page-data"])["curPage"]
            #构建url
            # if page_data['curPage'] < page_data['totalPage']:
            curr_page = soup.select_one('.curr-page')
            if curr_page :
                url = '{}p{}'.format(url_Tmp,str(int(curr_page.text)+1))
            
            # url = next_page['href']
        # next_page = soup.select_one('.next.next-active')
        # if next_page is not None:
        #     # 点击下一页按钮
        #     url = next_page['href']
        #     # 等待一段时间
        time.sleep(random_time / 1000)
# 关闭浏览器对象
browser.quit()
# 将数据存储到CSV文件中
df = pd.DataFrame(data, columns=['小区名', '地址', '建造年限'])
df.to_csv('lianjia_ershoufang.csv', index=False, encoding='utf-8-sig')
print("完成")