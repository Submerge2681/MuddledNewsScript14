from bs4 import BeautifulSoup
import requests
import csv
import re

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en"
    }

keywords = ['Modi', 'BJP', 'मोदी', 'बाजपा', 'मोदीजी', 'Modiji', 'बी जे पी', 'बी.जे.पी', 'B.J.P']
data = []

def grabber(soup_title, soup_body, soup, url):
    info = []
    article_time = soup.find('span', itemprop='dateModified').text
    article_time = article_time.replace('Updated:','').replace('IST','').replace('pm','').replace('am','')
    article_time = article_time.strip()[:-5]
    article_title = soup_title
    article_body = soup_body
    article_tags = soup.find('div', class_='tg_wrp').text.split()
    article_link = url
    info.append(article_time)
    info.append(article_title)
    info.append(article_body)
    info.append(article_tags)
    info.append(article_link)
    data.append(info)

def inspect_article(url):
    try:
        response = requests.get(url, headers = headers)
        # response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        soup_title = soup.find('h1').text.strip()
        soup_body = soup.find('div', id='ins_storybody').text
        # test_title = soup_title.split()
        test_body = soup_body.split()
        for i in keywords:
            if i in test_body:
                grabber(soup_title, soup_body, soup, url)
                break
    except Exception as e:
        print(f"Error fetching page content: {str(e)}")
        return None

def scriber(data):
    csv_file = "modi2014sep.csv"
    fieldnames = ['Date','Title','Body','Tags','Link']
    
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        for row in data:
            writer.writerow(row)
    print(f"Data has been written to {csv_file}.")

archive_url = 'https://archives.ndtv.com/articles/2014-09.html'

try:
    archive_main_page = requests.get(archive_url, headers = headers)
    main_page_body = BeautifulSoup(archive_main_page.content, 'html.parser')
    group = main_page_body.find('div', id='insidemidpanel')
    articles = group.find_all('li')
    for i in articles:
        url = i.find('a', href = True)['href']
        inspect_article(url)
except Exception as e:
        print(f"{str(e)}")
finally:
    scriber(data)