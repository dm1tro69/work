import codecs

import requests
from bs4 import BeautifulSoup as BS
import time

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
base_url = 'https://djinni.co/jobs/?primary_keyword=Python&location=Киев'

domain = 'https://djinni.co'
jobs =[]
urls = []
urls.append(base_url)
urls.append(base_url + '&page=2')
urls.append(base_url + '&page=3')

req = session.get(base_url, headers=headers)
# if req.status_code == 200:
#     bsObj = BS(req.content, 'html.parser')
#     pagination = bsObj.find('ul', attrs={'class': 'pagination'})
#     if pagination:
#         pages = pagination.find_all('li', attrs={'class': False})
#         for page in pages:
#             urls.append(domain + page.a['href'])
for url in urls:
    time.sleep(2)
    req = session.get(url, headers=headers)
    if req.status_code == 200:
        bsObj = BS(req.content, 'html.parser')
        li_list = bsObj.find_all('li', attrs={'class': 'list-jobs__item'})
        for li in li_list:
            div = li.find('div', attrs={'class': 'list-jobs__title'})
            title = div.a.text
            href = div.a['href']
            short = 'No description'
            #company = 'No name'
            descr = li.find('div', attrs={'class': 'list-jobs__description'})
            if descr:
                short = descr.p

            jobs.append({'href': domain + href,
                         'title': title,
                         'descript': short,
                         'company': 'No name'})




    #print(company)
    #print(div.find('p').text)


#data = bsObj.prettify()#.encode('utf8')
template = '<!doctype html><html lang="en"><head><meta charset="utf-8"></head><body>'
end = '</body></html>'
content = '<h2> djinni.co</h2>'
for job in jobs:
    content += '<a href="{href}" target="_blank">{title}</a><br/><p>{descript}</p><p>{company}</p><br/>'.format(**job)
    content += '<hr/><br/><br/>'
data = template + content + end
handle = codecs.open('jobs.html', "w", 'utf-8')
handle.write(str(data))
handle.close()