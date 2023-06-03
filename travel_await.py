import requests 
import httpx
import asyncio
import pandas as pd 
from bs4 import BeautifulSoup
import scraper_helper as sh
import csv
import time

def read_csv():
    url_1_list = []
    url_2_list = []
    data = pd.read_csv('data2.csv',encoding='cp1252',dtype='unicode')
    data = data.head(213)
    link_1 = data['link 1']
    link_2 = data['link 2']
    for urls_1 in link_1 :
        url_1_list.append(urls_1)
    for urls_2 in link_2:
        url_2_list.append(urls_2)
    return url_1_list

def get_text(url , soup):
    if 'thelocaltongue' in url:
        text = soup.select_one('p.subtitle.flipboard-subtitle.font-3').text.strip()
        print('thelocal')
    elif 'roadsandkingdoms.com' in url:
        text = soup.select_one('div.post-content.js-fitvids p').text.strip()
        print('road') 
    elif 'guide' in url:
        text = soup.select_one('.col-12:nth-child(1) .hotelpage__block').text.strip()
    elif 'insideosaka' in url:
        text = soup.select_one('div.entry-content p').text.strip()
    elif 'monocle' in url:
        text = soup.select_one('section.magazine-main-article.body-copy.truncated p').text.strip()
    elif 'afar' in url:
        text = soup.select_one('.RichTextBody > p').text.strip()
        print('afar')
    elif 'eater' in url:
        text = soup.select_one('div.c-entry-content.venu-card p').text.strip()
    elif 'japantimes' in url:
        text = soup.select_one('div#jtarticle p').text.strip()
    elif 'theinfatuation' in url:
        text = soup.select_one('p.styles_text__HThtH').text.strip()
    elif 'worlds50' in url:
        text = soup.select_one('div.content p').text.strip()
    else:
        text = 'else function'#soup.select_one('p')
    print(text)
    return text

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}

async def request(url):
    global r 
    text_list = []
    url_list  = []
    #global text
    async with httpx.AsyncClient() as clinet :
        try:
            r = await clinet.get(url , headers=headers)
            r.raise_for_status()
        
            soup = BeautifulSoup(r.content,'lxml')
            try:
                text = get_text(url,soup)
                print('done text')
            except AttributeError:
                text = 'attr'
        except httpx.HTTPError as http:
            text = print('http error')
            pass
        # print('attribtererror')
        text_list.append(text)
        url_list.append(url)
        return text_list,url_list
def saving_tocsv(output):
    df = pd.DataFrame(output)
    df.to_csv('my_data_async.csv',index=False,header=['text','url'])
    return        

async def main():
    result = []
    tasks = []
    for url in read_csv():
        tasks.append(asyncio.create_task(request(url)))
    output = await asyncio.gather(*tasks)
    for resluts in output:
        result.append(resluts)
    
    print(result)
    saving_tocsv(result)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())

