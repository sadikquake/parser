import requests
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

# parse of sections pages
def parse_section_page(url):
    sections = parse_main_page(url)
    if isinstance(sections, list) and len(sections):
        elements = []
        for section in sections:
            try:
                answer = get_answer(section[1])
                if answer:
                    soup = BeautifulSoup(answer, 'lxml')
                    ads_continers = soup.findAll('div', {'class': 'inzeraty inzeratyflex'})
                    if len(ads_continers):
                        for ad in ads_continers:
                            name = ad.find('h2', {'class': 'nadpis'}).find('a').text
                            desc = ad.find('div', {'class': 'popis'}).text
                            date = ad.find('span', {'class': 'velikost10'}).text
                            price = ad.find('div', {'class': 'inzeratycena'}).find('b').text.strip()
                            count_views = ad.find('div', {'class': 'inzeratyview'}).text
                            elements.append([name, desc, date, price, count_views])
                    else:
                        print('Ads not found')
            except:
                print('The response of the requested section was not received')
    else:
        print('Sections not found')


