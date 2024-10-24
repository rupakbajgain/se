#University of Michigan(Not Implemented*)

def main(config):
    print("not implemented")
    return []

"""
page = 'https://cee.engin.umich.edu/role/faculty'
print("Not Implemented")
#bcz i already did the email with previous version

@persist("professors")
def get_professors():
    print(f'Starting url: {page}')
    all_links=set()
    p = Page(page)
    all_pages=[p]
    for i in p.get_soup().find_all("a", class_="page-numbers"):
        u=page+i['href']
        all_links.add(u)
    print(f'No of pages: {len(all_links)+1}')
    for i in all_links:
        all_pages.append(Page(i))
    def get_main_info(s,url):
        p=[]
        for i in s.find_all('li',class_='people'):
            info = {}
            info['name'] = i.find('h2').string
            info['info'] = i.find('p').string
            if 'emeritus' in info['info'].lower():#retired jst skip
                continue
            info['link'] = i.find('a')['href']
            info['ref'] = url
            p.append(info)
        return p
    #def get professors list
    peoples=[]
    for s in all_pages:
        peoples += get_main_info(s.get_soup(),s.url)
    print(f"{len(peoples)} professors found")
    return peoples
"""