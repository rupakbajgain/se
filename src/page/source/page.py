from .cfetch import CFetch
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from urllib.parse import urlparse,urldefrag,unquote

#top level page managing class
class Page:
    def __init__(self,url,history=[],depth=0):
        self.url = url
        self.history = history
        self.soup = None
        self.__url = None
        self.depth = depth
        self.__cfetch = CFetch(url)
    
    def goto(self,newurl):#new page with this history
        return Page(urljoin(self.url, newurl),history=self.history+[self.url],depth=self.depth+1)
    
    #c= no of pages back
    def get_last_history(self,c=1):
        l = len(self.history)
        if l:
            return self.history[l-c]

    def fetch(self,**k):
        #return self.__cfetch.fetch(**k)
        try:
            return self.__cfetch.fetch(**k)
        except:
            return False

    def head(self):
        return self.__cfetch.head()
    
    def get_soup(self):
        if not self.soup:
            r=self.fetch()
            if r:
                self.soup = BeautifulSoup(r,features="html.parser")
            else:
                print("Got no response")
                self.soup = BeautifulSoup(f"Page not found! {self.url}",features="html.parser")
        return self.soup
    
    def get_all_links(self):
        links=[]
        if not self.get_soup():
            return links
        for i in self.soup.find_all('a'):
            h=i.get('href')
            if h:
                links.append(urljoin(self.url, i['href']))
        return links
    
    def get_url(self):#returns url but parsed
        if not self.__url:
            self.__url = urlparse(self.url)
        return self.__url

    #better all_links
    def get_filtered_links(self,page=None,links=None,url=None,filter=True):
        links1 = self.get_all_links()
        if not links:
            if not page:
                if not url:#get url
                    l = self.get_url()
                    if l.path=='/':#this is root page
                        for i in links1:
                            k=urlparse(i)
                            if k.netloc == l.netloc:
                                if k.path==l.path:
                                    continue
                                else:
                                    url=i
                                    break
                        return []#out of ideas
                    else:
                        url = l.scheme + '://' + l.netloc
                    page = Page(url)
                links = page.get_all_links()
        sl=set()
        for i in links1:
            if i not in links:
                if filter:
                    sl.add(unquote(urldefrag(i)[0]))
                else:
                    sl.add(i)
        return sl
