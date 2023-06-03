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
    data = data.head(5)
    link_1 = data['link 1']
    link_2 = data['link 2']
    for urls_1 in link_1 :
        url_1_list.append(urls_1)
    for urls_2 in link_2:
        url_2_list.append(urls_2)
    return url_1_list
    
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}

def request(url):
    global r 
    try:
        r = httpx.get(url , headers=headers)
        r.raise_for_status()
    except requests.exceptions.HTTPError as http:
        print(http)
        pass
    except requests.exceptions.ConnectionError as conn:
        print(conn)
        pass
    except requests.exceptions.MissingSchema as sh:
        print(sh)
        pass
    except requests.exceptions.ReadTimeout as timeout:
        print(timeout)
        pass
    #time.sleep(2)
    return r.content
def extract(content):
    text_list = []
    url_list  = []
    soup = BeautifulSoup(content,'lxml')
    try:
        text = soup.find('p').text.strip()
    except AttributeError:
        text = 'none'
    text_list.append(text)
    url_list.append(url)
    #print(data_text)
    return text_list,url_list
def saving_tocsv(output):
    df = pd.DataFrame(output)
    df.to_csv('my_data.csv',index=False,header=['text','url'])
    # with open('my_data.csv' ,'a+')as f:
    #     csv_writer = csv.DictWriter(f , fieldnames=['text','url'])
    #     csv_writer.writeheader
    #     for key,values in output:
    #         csv_writer.writerow(key,values)
    return        

result = []
for url in read_csv():
    scraped = request(url)
    #print(scraped)
    output = extract(scraped)
    print(output)
    result.append(output)
print(result)

# saving_tocsv(result)
    


    
        
    



