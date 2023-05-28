import requests, math, sys
from bs4 import BeautifulSoup
from datetime import date

# message language
lang = 'en'
# log file
log = './logs/' + str(date.today()) + '.log'

# get answer from url
def get_answer(url = ''):
    url = url.strip()
    if url:
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/113.0.0.0 Safari/537.36'}
        try:
            responce = requests.get(url, headers = header)
            if responce.text:
                if responce.status_code == 200:
                    return responce.text
                else:
                    write_file(log, 'Answer is wrong\n')
            else:
                write_file(log, 'Answer is empty\n')
        except:
            write_file(log, 'Unable to get a response\n')
    else:
        write_file(log, 'Empty url\n')

# parse of the main page
def parse_main_page(url):
    try:
        answer = get_answer(url)
        sections = []
        soup = BeautifulSoup(answer, 'lxml')
        container = soup.find('div', {'class': 'sirka'})
        sections_containers = container.findAll('span', {'class': 'nadpisnahlavni'})
        if sections_containers:
            for i in sections_containers:
                sections.append([i.text, i.find('a').get('href')])
            return sections
        else:
            write_file(log, 'No sections found\n')
    except:
        write_file(log, 'Can\'t parse of the main page\n')

# collecting the urls of all pages
def get_all_url(sections):
    if isinstance(sections, list) and len(sections):
        urls = ''
        urls_file = './data/urls.txt'
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
                        if not i:
                            urls += section[1] + '\n'
                        else:
                            urls += section[1] + str(i * count_ads_page) + '/\n'
                        i += 1
                else:
                    write_file(log, 'Unable to get information about the section\n')
            except:
                write_file(log, 'The response of the requested section was not received\n')
        if urls:
            write_file(urls_file, urls)
    else:
        write_file(log, 'Sections not found\n')

# service functions
# writing file
def write_file(file_name = '', data = ''):
    file_name = file_name.strip()
    data = data.strip()
    if file_name and data:
        try:
            with open(file_name, 'a') as f:
                f.write(data)
                f.close()
        except:
            print('Unable to write data to file')
    else:
        write_file(log, 'No file name or data to write is specified\n')

# clearing the variable
def clearning_var(var, type = 'int'):
    match type:
        case 'date':
            new_var = ''.join((x for x in var if x.isdigit() or x == '.'))
        case 'int' | _:
            new_var = ''.join((x for x in var if x.isdigit()))
    return new_var

# checking of requirements
def check_requirements():
    if not (sys.version_info.major == 3 and sys.version_info.minor >= 10):
        print('You need python version 3.10 or higher')

