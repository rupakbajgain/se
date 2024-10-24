from ...page import Page
from scholarly import scholarly
import logging

def get_prof_datas(prof):
    logging.info('title','Scholar search')
    logging.info('msg','Starting scholar search')
    search_query = scholarly.search_author(prof['name'])
    ba = None#just for backup
    c = 0
    author = None
    for i in search_query:
        c+=1
        #print(i)
        if c==1:
            ba = i
        d = i.get('email_domain')
        if not d:
            continue
        if len(d) and prof['email'].endswith(d):
            author = i
            break
    ##print(author,ba,c)
    #exit()
    if c==1 and not author and False:
        print('Name not found on scholar')
        author=ba
    if not author:
        return False
    logging.info('msg',f'Author url: https://scholar.google.com/citations?hl=en&user={author["scholar_id"]}')
    author = scholarly.fill(author,sections=['basics', 'publications'])#load more
    top_article = author['publications'][0]
    if len(author['publications'])>1:
        top_article1 = author['publications'][1]
    recent_article = None
    year = 0
    for i in author['publications']:
        pyear = i['bib'].get('pub_year')
        if pyear:
            pyear = int(pyear)
        else:
            continue
        if pyear>year:
            recent_article = i
            year = pyear

    #load more
    top_article = scholarly.fill(top_article)
    #top_article1 = scholarly.fill(top_article1)
    #print(top_article)
    recent_article = scholarly.fill(recent_article)
    #articles = [top_article, top_article1, recent_article]
    articles = [top_article, recent_article]
    if top_article1:
        articles.append(scholarly.fill(top_article1))
    links = []
    #print("---")
    for  i in articles:
        logging.info('msg',i['bib']['title'])
        ref = f'https://scholar.google.com/citations?view_op=view_citation&hl=en&user={author["scholar_id"]}&citation_for_view={i["author_pub_id"]}'
        #print(ref)
        article = i.get('pub_url')
        if not article:
            continue
        #print(article)
        Page(article).fetch()#dont need in this step, just old convection to make faster
        #print("---")
        if not i['bib'].get('journal'):
            i['bib']['journal']=''
        if not i['bib'].get('abstract'):
            i['bib']['abstract']=''
        links.append({'title':i['bib']['title'],'intro': f"# Publication title: {i['bib']['title']}\nPublish Year:{i['bib']['pub_year']}\nCitation:{i['bib']['citation']}\nJournal:{i['bib']['journal']}  \n\n"+i['bib']["abstract"], 'ref': ref,'link': article})
    return links