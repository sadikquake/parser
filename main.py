import requests, math
from bs4 import BeautifulSoup

# get answer from url
def get_answer(url = ''):
    url = url.strip()
    if len(url):
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/113.0.0.0 Safari/537.36'}
        try:
            responce = requests.get(url, headers=header)
            if len(responce.text):
                if responce.status_code == 200:
                    return responce.text
                else:
                    print('Answer is wrong')
            else:
                print('Answer is empty')
        except:
            print('Unable to get a response')
    else:
        print('Empty url')

# parse of the main page
def parse_main_page(url):
    try:
        answer = get_answer(url)
        sections = []
        soup = BeautifulSoup(answer, 'lxml')
        container = soup.find('div', {'class': 'sirka'})
        sections_containers = container.findAll('span', {'class': 'nadpisnahlavni'})
        if len(sections_containers):
            for i in sections_containers:
                sections.append([i.text, i.find('a').get('href')])
            return sections
        else:
            print('No sections found')
    except:
        print('Can\'t parse of the main page')

# collecting the urls of all pages
def get_all_url(sections):
    if isinstance(sections, list) and len(sections):
        urls = []
        for section in sections:
            try:
                answer = get_answer(section[1][:-1])
                if answer:
                    soup = BeautifulSoup(answer, 'lxml')
                    count_ads = soup.find('div', {'class': 'inzeratynadpis'}).text.strip().split(' z ')[1]
                    count_ads = int(count_ads.replace(' ',''))
                    count_ads_page = len(soup.findAll('div', {'class': 'inzeraty inzeratyflex'}))
                    count_all_pages = math.ceil(count_ads / count_ads_page)
                    i = 0
                    while i < count_all_pages:
                        urls.append(section[1] + str(i * count_ads_page) + '/')
                        i += 1
                else:
                    print('Unable to get information about the section')
            except:
                print('The response of the requested section was not received')
    else:
        print('Sections not found')