#https://www.work.ua/jobs-kyiv-python/
import requests
from bs4 import BeautifulSoup as BS

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
base_url = 'https://www.work.ua/jobs-kyiv-python/'

domain = 'https://www.work.ua'
jobs =[]
urls = []
urls.append(base_url)
req = session.get(base_url, headers=headers)
if req.status_code == 200:
    bsObj = BS(req.content, 'html.parser')
    pagination = bsObj.find('ul', attrs={'class': 'pagination'})
    if pagination:
        pages = pagination.find_all('li', attrs={'class': False})
        for page in pages:
            urls.append(domain + page.a['href'])

# if req.status_code == 200:
#     bsObj = BS(req.content, 'html.parser')
#     div_list = bsObj.find_all('div', attrs={'class': 'job-link'})
#     for div in div_list:
#         title = div.find('h2')
#         href = title.a['href']
#         short = div.p.text
#         company = 'No name'
#         logo = div.find('img')
#         if logo:
#             company = logo['alt']
#         jobs.append({'href': domain + href,
#                      'title': title.text,
#                      'descript': short,
#                      'company': company})




    #print(company)
    #print(div.find('p').text)


#data = bsObj.prettify()#.encode('utf8')
handle = open('urls.html', 'w', encoding='utf-8')
handle.write(str(urls))

handle.close()