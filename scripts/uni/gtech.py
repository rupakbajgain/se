#Georgia Tech
from src.page import Page
import logging

base = 'https://ce.gatech.edu/people'
#logging.info('Starting on page '+ page)

def findmail(soup):
    for i in soup.find_all('a'):
        h = i.get('href')
        if not h:
            continue
        if h.startswith('mailto:'):
            return i.string

#name,position,email,university,bio,ref

def get_professors():
    logging.info(f'Starting url: {base}')
    page = Page(base)
    soup = page.get_soup()
    pages=[page]
    for i in soup.find_all('a',class_='pager__link'):
        if 'is-active' in i['class']:
            continue
        p2=page.goto(i['href'])
        pages.append(p2)
    pages=pages[:-2]
    profs = []
    logging.info('Pages', len(pages))
    for i in pages:
        s=i.get_soup()
        for j in s.find_all('div', class_='node--type-dir-person'):
            info={} 
            info['name']=j.find('div',class_='field--type-name').text.strip()
            #logging.info(info['name'])
            pos = j.find('div',class_='field--name-field-person-job-title-s-')
            pos=pos.text.strip()
            info['position']=pos
            pos=pos.lower()
            if not 'professor' in pos:
                continue
            if 'emeritus' in pos:
                continue
            info['university']='Georgia Tech'
            info['ref']=i.url
            link =  j.find('a')
            px = i.goto(link['href'])
            info['bio']=px.url
            info['email']=findmail(px.get_soup())
            if not info['email']:
                continue
            logging.info(info['name'])
            profs.append(info)
    return profs

def main(config):
    return get_professors()