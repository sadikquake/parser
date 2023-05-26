import requests
from bs4 import BeautifulSoup

def get_answer(url = ''):
    url = url.strip()
    if len(url):
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/113.0.0.0 Safari/537.36'}
        try:
            responce = requests.get(url, headers=header).text
            if len(responce):
                pass
            else:
                print('Answer is empty')
        except:
            print('Unable to get a response')
    else:
        print('Empty url')