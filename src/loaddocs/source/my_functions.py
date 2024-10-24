import hashlib,os
from .loader import HTMLLoader
#from helper.counter import currentCounter,setCounter

from langchain_community.document_loaders import PyPDFLoader
from langchain_unstructured import UnstructuredLoader
#UnstructuredLoader dont work as expected, not comple output for text file
#just skipping warning: by doing what is says
from langchain_core.documents import Document
from .word import count_words
from ...config import getConfig
import logging

config = getConfig()
download_path = config['directories']['DOWNLOAD_PATH']

def md5_loader(url):
    hash = hashlib.md5(url.encode()).hexdigest()
    file_path = os.path.join(download_path, hash)
    return file_path

def doctype(filename):
    with open(filename, 'br') as f:
        data = f.read(4)
        if data==b'%PDF':
            return 'pdf'
        if data[:2]==b'<!' or data[:2]==b'<H' or data[:2]==b'<h':
            return 'html'
        return False

def prof_to_doc(prof):
    if not prof['position']:
        prof['position']=''
    return f"Info\n\nName : {prof['name']}\nRole : {prof['position']}\nEmail : {prof['email']}"

#profs = getprofessors()
def get_documents(links):
    #create 1 intro doc
    documents=[]

    #print(len(prof_['l']))
    ls = links
    for i in ls:
        logging.info(f"Loading {i['link']}")#, end=' ')
        try:
            f=md5_loader(i['link'])
            ftype = doctype(f)
            if ftype=='pdf':
                #print('[PDF]')
                loader = PyPDFLoader(f)
            elif ftype=='html':
                #print('[HTML]')
                loader = HTMLLoader(i['link'],f)#provide URL instead, f for formating only
            else:
                #print('[O]')
                loader = UnstructuredLoader(f)
            d = loader.load()[0]
            k = d.page_content.find('efrences')#missing r
            if k!=-1:
                d.page_content=d.page_content[0:k-1]
            d.metadata['link'] = i['link']
            d.metadata['ref'] = i['ref']
            if i.get('single_page'):
                #print('got single')
                d.metadata['single_page'] = True
            if i.get('intro'):
                d.metadata['intro'] = i['intro']
            if i.get('title'):
                d.metadata['title'] = i['title']
            #print(d)
            #print(d.metadata)
            documents.append(d)
        except Exception as error:
            #print(error)
            logging.debug(error)

    #print(len(documents), "documents loaded")
    return documents

#main keywords to search in documents]
MAX_LENGTH = 1000 #slice if more than this
article_keywords = ['keywords','introduction', 'conclusion','acknowledgement','appendices','references']#abstract add manually
scholar_keywords = ['title','description','citations']#citation means total citations
#more_keywords = ['education','teaching','total','show','interests','email']#general; better use ,'email' as regex, 'total citations' 'see more'
more_keywords = ['teaching','interests']
research_gate_keywords = ['publications','network']
project_keywoards = ['mission','team','advisors','partners']
#faculty_page_finder = ['professor','lecturer']
main_keywords=article_keywords+scholar_keywords+more_keywords+research_gate_keywords+project_keywoards#+faculty_page_finder
#dont focus on keyword publication keyword too general

tracked_keywords = ['abstract','conclusion','title','interests','expertise','news']

def _get_content(d,sv,c):
    ec = len(d)
    s = sv-20
    if s<0:
        s=0
    if s<0:
        s=0
    for _,l in c.items():
        for v in l:
            if v>sv and v<ec:
                ec=v
    if ec-sv>MAX_LENGTH:
        ec = sv+MAX_LENGTH
    return d[s: ec]

def _format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

FILTER_CONTENTS = False
def docs_to_text(documents):
    docs = []
    for i in documents:
        if i.metadata.get('single_page'):
            docs.append(i)#single page manual request
            #print('got single')#---------------
            continue
        if i.metadata.get('intro'):
            docs.append(Document(page_content=i.metadata['intro'],metadata=i.metadata))
            if not FILTER_CONTENTS:
                docs.append(i)
                continue
            counts = count_words(i.page_content,main_keywords)    
        else:
            if not FILTER_CONTENTS:
                docs.append(i)
                continue
            counts = count_words(i.page_content,main_keywords+['abstract'])#dont double intro
        cs=[]
        for k,l in counts.items():
            #print(k)
            if not k  in tracked_keywords:
                continue
            for v in l:
                c = _get_content(i.page_content, v, counts)
                cs.append(c)
        for l in cs:
            docs.append(Document(page_content=l,metadata=i.metadata))
    fd = _format_docs(docs)
    #if len(fd)>7*MAX_LENGTH:
    #    fd=fd[:7*MAX_LENGTH]#clamp it
    logging.info(f'{len(fd)} characters used for summay')
    return fd

