import requests
from bs4 import BeautifulSoup
import sys

def main():
    url = 'https://www.baidu.com'
    response = requests.get(url)
    html = response.content 
    soup = BeautifulSoup(html, 'html.parser')
    # 获取所有的链接
    links = [link.get('href') for link in soup.find_all('a')]
    # 获取所有的文本
    texts = [text.get_text() for text in soup.find_all('p')]
    with open('links.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(links))
        
    with open('texts.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(texts))

if __name__ == "__main__" :
    main()