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

# parse of main page
def parse_main_page(url):
    try:
        answer = get_answer(url)
        sections = []
        soup = BeautifulSoup(answer, 'lxml')
        container = soup.find('div', {'class': 'sirka'})
        sections_containers = container.findAll('span', {'class': 'nadpisnahlavni'})
        if len(sections_containers):
            for i in sections_containers:
                sections.append([i.text, i.select('a')[0]['href']])
            return sections
        else:
            print('No sections found')
    except:
        print('Can\'t parse of main page')
