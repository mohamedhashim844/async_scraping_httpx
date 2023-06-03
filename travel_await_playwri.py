from playwright.async_api import async_playwright
import requests 
import httpx
import asyncio
import pandas as pd 
from bs4 import BeautifulSoup
import scraper_helper as sh
import csv
import time

async def playwrght(url):
    plyaywr_text = []
    playwr_url = []
    #url = 'https://goop.com/place/mexico/mexico-city/polanco-hotels/las-alcobas/'
    ua = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/69.0.3497.100 Safari/537.36"
    )
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=ua)
        await page.goto(url,timeout=0)
        #page.wait_for_timeout(1000)
        html = await page.content()
        soup = BeautifulSoup(html , 'lxml')
        try :
            text = soup.find('p').text.strip()
        except AttributeError :
            text = 'none'
        plyaywr_text.append(text)
        playwr_url.append(url)
        return plyaywr_text , playwr_url

def read_csv():
    url_1_list = []
    url_2_list = []
    data = pd.read_csv('data2.csv',encoding='cp1252',dtype='unicode')
    data = data[10:18]
    link_1 = data['link 1']
    link_2 = data['link 2']
    for urls_1 in link_1 :
        url_1_list.append(urls_1)
    for urls_2 in link_2:
        url_2_list.append(urls_2)
    return url_1_list
    
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}

async def request(url):
    text_list = []
    url_list  = []
    global r 
    async with httpx.AsyncClient() as clinet :
        try:
            r = await clinet.get(url , headers=headers)
            r.raise_for_status()
        except httpx.HTTPStatusError as http:
            print(http)
            pass
        except httpx.ConnectError as conn:
            print(conn)
            pass
        except httpx.ReadTimeout as sh:
            print(sh)
            pass
        except httpx.ConnectTimeout as timeout:
            print(timeout)
            pass
        soup = BeautifulSoup(r.content,'lxml')
        try:
            text = soup.find('p').text.strip()
        except AttributeError:
            text = 'none'
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
    # for url in read_csv():
    #     if 'goop' not in url :
    #         tasks.append(asyncio.create_task(request(url)))
    # output = await asyncio.gather(*tasks)
    for url in read_csv():
        if 'goop' in url:
            print(url)
            tasks.append(asyncio.create_task(playwrght(url)))
            print(tasks)
    output = await asyncio.gather(*tasks)
    
        
    for resluts in output:
        result.append(resluts)
    
    print(result)
    #saving_tocsv(result)

asyncio.run(main())