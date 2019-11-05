import codecs

import requests
from bs4 import BeautifulSoup as BS
import time
import datetime

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
base_url = 'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2?period=3&lastdate='

domain = 'https://rabota.ua'
jobs =[]
urls = []
yesterday = datetime.date.today()-datetime.timedelta(1)
one_day_ago = yesterday.strftime('%d.%m.%Y')
base_url = base_url + one_day_ago
urls.append(base_url)


req = session.get(base_url, headers=headers)
if req.status_code == 200:
    bsObj = BS(req.content, 'html.parser')
    pagination = bsObj.find('dl', attrs={'id': 'ctl00_content_vacancyList_gridList_ctl23_pagerInnerTable'})
    if pagination:
        pages = pagination.find_all('a', attrs={'class': 'f-always-blue'})
        for page in pages:
            urls.append(domain + page['href'])
for url in urls:
    time.sleep(2)
    req = session.get(url, headers=headers)
    if req.status_code == 200:
        bsObj = BS(req.content, 'html.parser')
        table = bsObj.find('table', attrs={'id': 'ctl00_content_vacancyList_gridList'})
        if table:
            tr_list = bsObj.find_all('tr', attrs={'id': True})
            for tr in tr_list:
                h3 = tr.find('h3', attrs={'class': 'f-vacancylist-vacancytitle'})
                title = h3.a.text
                href = h3.a['href']
                short = 'No description'
                company = 'No name'
                logo = tr.find('p', attrs={'class': 'f-vacancylist-companyname'})
                if logo:
                    company = logo.a.text
                p = tr.find('p', attrs={'class': 'f-vacancylist-shortdescr'})
                if p:
                    short = p.text

                jobs.append({'href': domain + href,
                             'title': title,
                             'descript': short,
                             'company': company})




    #print(company)
    #print(div.find('p').text)


#data = bsObj.prettify()#.encode('utf8')
template = '<!doctype html><html lang="en"><head><meta charset="utf-8"></head><body>'
end = '</body></html>'
content = '<h2> rabota.ua</h2>'
for job in jobs:
    content += '<a href="{href}" target="_blank">{title}</a><br/><p>{descript}</p><p>{company}</p><br/>'.format(**job)
    content += '<hr/><br/><br/>'
data = template + content + end
handle = codecs.open('jobs.html', "w", 'utf-8')
handle.write(str(data))
handle.close()