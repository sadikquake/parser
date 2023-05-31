import requests, math, sys, csv
from bs4 import BeautifulSoup
from datetime import date, datetime

url = 'https://www.bazos.cz'
lang = 'en'
log = './logs/' + str(date.today()) + '.log'
datetime_now = datetime.now()
time_now = str(datetime_now.hour) + ':' + str(datetime_now.minute) + ':' + str(datetime_now.second)
data_dir = './data/'
urls_list = data_dir + 'urls.txt'
urls = []

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
                    write_file(log, time_now + ' Answer is wrong, answer code is ' + str(responce.status_code) + '\n')
            else:
                write_file(log, time_now + ' Answer is empty, url is ' + url + '\n')
        except:
            write_file(log, time_now + ' Unable to get a response\n')
    else:
        write_file(log, time_now + ' Empty url\n')

# parse of the main page
def parse_main_page():
    try:
        answer = get_answer(url)
        sections = []
        soup = BeautifulSoup(answer, 'lxml')
        container = soup.find('div', {'class': 'sirka'})
        sections_containers = container.findAll('span', {'class': 'nadpisnahlavni'})
        if sections_containers:
            for i in sections_containers:
                sections.append(i.find('a').get('href'))
            return sections
        else:
            write_file(log, time_now + ' No sections found, url is ' + url + '\n')
    except:
        write_file(log, time_now + ' Can\'t parse of the main page (url is ' + url + ')\n')

# collecting the urls of all pages
def get_all_url():
    sections = parse_main_page()

    if isinstance(sections, list) and len(sections):
        urls = ''
        for section in sections:
            try:
                answer = get_answer(section[:-1])
                if answer:
                    soup = BeautifulSoup(answer, 'lxml')
                    count_ads = soup.find('div', {'class': 'inzeratynadpis'}).text.strip().split(' z ')[1]
                    count_ads = int(count_ads.replace(' ',''))
                    count_ads_page = len(soup.findAll('div', {'class': 'inzeraty inzeratyflex'}))
                    count_all_pages = math.ceil(count_ads / count_ads_page)
                    i = 0
                    while i < count_all_pages:
                        if not i:
                            urls += section + '\n'
                        else:
                            urls += section + str(i * count_ads_page) + '/\n'
                        i += 1
                else:
                    write_file(log, time_now + ' Unable to get information about the section\n')
            except:
                write_file(log, time_now + ' The response of the requested section was not received\n')
        if urls:
            write_file(urls_list, urls, 'w')
    else:
        write_file(log, time_now + ' Sections not found\n')

# parse of the section pages
def parse_section_page():
    try:
        with open(urls_list, 'r') as f:
            url = f.readline()
            while url:
                try:
                    answer = get_answer(url)
                    if answer:
                        soup = BeautifulSoup(answer, 'lxml')
                        title = soup.find('h1').text.strip()
                        ads_continers = soup.findAll('div', {'class': 'inzeraty inzeratyflex'})
                        if len(ads_continers):
                            elements = []
                            for ad in ads_continers:
                                name = ad.find('h2', {'class': 'nadpis'}).find('a').text
                                #desc = ad.find('div', {'class': 'popis'}).text
                                date = clearning_var(ad.find('span', {'class': 'velikost10'}).text, 'date')
                                price = ad.find('div', {'class': 'inzeratycena'}).find('b').text.strip()
                                count_views = clearning_var(ad.find('div', {'class': 'inzeratyview'}).text)
                                elements.append(name + '\n' + date + '\n' + price + '\n' + count_views + '\n\n')
                            write_file(data_dir + str(title) + '.txt', ''.join(elements))
                        else:
                            write_file(log, time_now + ' Ads not found\n')
                except:
                    write_file(log, time_now + ' The response of the requested section was not received\n')
                url = f.readline()
            f.close()
    except:
        write_file(log, time_now + ' Unable to read url addresses from file\n')

# service functions
# writing file
def write_file(file_name = '', data = '', mode = 'a+'):
    file_name = file_name.strip()
    data = data.strip()
    if file_name and data:
        try:
            with open(file_name, mode, encoding='utf-8') as f:
                f.write(data)
                f.close()
        except:
            print('Unable to write data to file ' + file_name)
    else:
        write_file(log, time_now + ' No file name or data to write is specified\n')

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
