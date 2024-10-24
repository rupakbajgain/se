#UC Berkeley
from src.page import Page
import logging

base = 'https://ce.berkeley.edu/people/faculty'
#logging.info('Starting on page '+ page)


#name,position,email,university,bio,ref

def get_professors():
    logging.info(f'Starting url: {base}')
    page = Page(base)
    soup = page.get_soup()
    p=[]
    for i in soup.find_all(class_='views-field-field-faculty-info'):
        info = {}
        l=i.find('a')
        info['name']=l.text.strip()
        logging.info(l['title'])
        info['position']=i.find('span',class_='bold').string
        info['university']='UC Berkeley'
        info['ref']=base
        page2 = page.goto(l['href'])
        info['bio']=page2.url
        soup2 = page2.get_soup()
        email=None
        #print(soup2)
        for i in soup2.find_all('a'):
            h = i.get('href')
            if not h:
                continue
            if h.startswith('mailto:'):
                email=i.string
        if not email:
            continue
        info['email']=email
        p.append(info)
    return p

def main(config):
    return get_professors()