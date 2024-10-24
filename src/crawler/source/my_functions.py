from ...page import Page
#from helper.counter import currentCounter
from .crawler import start_crawler
from urllib.parse import urlparse
import logging

#these sites take 1 shot
single_shots = [
    'www.etla.fi',
    'www.facebook.com',
    'www.youtube.com',
    'www.microsoft.com',
]

black_list = [
    'drive.google.com',
    'www.google.com',
    'accounts.google.com',
    'www.wix.com',
    'books.google.com',
    'github.com',
    'mademistakes.com',
    'jekyllrb.com',
    'www.twitter.com',#there were some exceptions for sites that dont exist
    'goo.gl',
    'www.apple.com',
    'support.google.com',
    'scholar.google.com',#we have diffrent part for it
]

import time
timeout = None
def determine_rule(p):
    global timeout
    if timeout-time.time()<0:
        return 'pass'

    if p.url.startswith('javascript:'):
        return 'pass'
    l=p.get_url()

    if l.path=='/' and p.depth>1:
        return 'pass'

    #general black and whitelists
    if l.netloc in black_list:
        return 'pass'
    if l.netloc in single_shots:
        return 'single'
    l1 = urlparse(p.get_last_history())

    #if diffrent root url provided in home page, it is bcz it is their site
    #general
    #print(l)
    if p.depth==0:
        return 'continue'
    elif p.depth>3:
        if l1.netloc!='scholar.google.com':
            # in scholar site jst continue
            logging.debug("Max depth reached")
            return 'single'
    elif l.scheme!='http' and l.scheme!='https':
        return 'pass'
    elif l.path.endswith('.pdf'):
        return 'single_req'

    if len(p.history)==2:
        if l.netloc != l1.netloc:
            return 'continue_personal'

    #general personal pages
    if l.netloc.endswith('github.io'):
        if l.path != '/':
            return 'single'
        return 'continue_personal'
    elif l.netloc.endswith('wixsite.com'):
        if l.path != '/':
            return 'single'
        return 'continue_personal'
    elif l.netloc=='sites.google.com':
        if l.path != '/':
            return 'single'
        return 'continue_personal'

    #if it want to go back cancel it
    k = l.netloc+l.path
    if k[-1]=="/":
        k=k[:-1]
    for i in p.history:
        if k in i:#i>l
            return 'pass'

    if l1.path=='/':
        return 'single'

    return 'single'

# application/pdf in head
# scholar.google.com fix, 1st time list, 2nd time description, 3rd time external link if available

def crawl_info(prof):
    global timeout
    timeout=time.time()+60#in sec
    #print(prof)
    if isinstance(prof['bio'], list):
        urls=prof['bio']
    else:
        urls=[prof['bio']]
    links=[]
    for i in urls:
        start_page=Page(i,history=[prof['ref']])
        if prof.get('single_page'):
            start_page.depth=100
        pages = start_crawler(start_page,determine_rule)
        for i in pages:
            links.append({'link':i.url,'ref':i.get_last_history()})
        if prof.get('single_page'):
            #print(len(links))
            links[0]['single_page']=True
        #print(links)
    links.reverse()
    return links
