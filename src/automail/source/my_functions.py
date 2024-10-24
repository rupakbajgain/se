from ...scholar import get_prof_datas as get_scholar_datas
from ...crawler import crawl_info
#from ...page import start_browser
from ...loaddocs import docs_to_text,get_documents
from ...createmail import docs_to_email
from ...sendmail import send_email

def automail(prof,demo=False):
    #start_browser()#lets use real browser, why not??
    #open browser in main program not in this library
    r = crawl_info(prof)
    r2 = get_scholar_datas(prof)

    if not r:
        r=r2
        if not r:
            return False
    elif r2:
        r += r2

    docs = get_documents(r)

    fd = docs_to_text(docs)

    mail = docs_to_email(fd, prof)
    if demo:
        prof['email'] = 'nnew234567@gmail.com'# cant do with test as scholar needs actual mail to work
    #print(mail)
    #throw(123)
    send_email(mail[1], mail[0], prof['email'])
    return True