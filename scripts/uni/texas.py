#University of Texas at Austin
import os,logging

page = 'https://www.caee.utexas.edu/people/faculty/faculty-directory'
#logging.info('Starting on page '+ page)

#name,position,email,university,bio,ref
import requests
from bs4 import BeautifulSoup
def fetch(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    return response.content

def get_professors():
    print(f'Starting url: {page}')
    r = fetch(page)
    #with open('test.html','w') as f:
    #    f.write(r)
    soup = BeautifulSoup(r,features="html.parser")
    p=[]
    for i in soup.find_all(class_='facinfo'):
        info = {}
        info['name'] = i.find('h4').string
        info['position'] = i.find('p',class_='facpos').string
        if 'emeritus' in info['position'].lower():#retired jst skip
            continue
        info['email'] = i.find('a',class_='email')
        if not info['email']:
            continue
        info['email'] = info['email'].string
        info['university'] = 'University of Texas at Austin'
        info['bio'] = 'https://www.caee.utexas.edu'+i.find('h6').find('a')['href']
        info['ref'] = page
        p.append(info)
    return p

def main(config):
    return get_professors()