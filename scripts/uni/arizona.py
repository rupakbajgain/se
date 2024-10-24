#Arizona State University
import os,logging

page = 'https://faculty.engineering.asu.edu/directory/ssebe/'
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
    l=[]
    p=[]
    for i in soup.find_all('a'):
        if i.get('href'):
            if 'ssebe' in i['href'] and not 'rank' in i['href']:
                l.append(i['href'])
    for ii in l:
        print(ii)
        r=fetch(ii)
        soup = BeautifulSoup(r,features="html.parser")
        for i in soup.find_all(class_='person'):
            name_link = i.find('a')
            info={}
            info['name'] = name_link.string
            info['bio'] = name_link['href']
            pos = i.find(class_='person-profession')
            if not pos:
                continue
            info['position'] = pos.getText()
            email = i.find('a', attrs={"aria-label": "Email user"})
            info['email'] = email['data-ga']
            info['university'] = 'Arizona State University'
            info['ref'] = ii
            p.append(info)
    return p

def main(config):
    return get_professors()

if __name__=="__main__":
    print(main([]))
