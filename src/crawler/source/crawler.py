import validators
import logging

def start_crawler(req,determine_rule):
    pages=[req]
    all_pages=[]#all crawled pages
    logging.info('title','Started crawler')
    while len(pages):
        page=pages.pop()
        foundX=False
        for i in all_pages:
            if page.url==i.url:
                foundX=True
        if foundX:
            continue
        rule=determine_rule(page)
        #print(f"Crawling url!({rule}): {page.url} ; {page.get_last_history()}")
        if rule=='pass':
            continue
        if not validators.url(page.url):
            continue
        logging.info('msg',f"Crawling url({rule}): {page.url} ; {page.get_last_history()}")
        match rule:
            case 'continue':
                r=page.get_filtered_links()
                all_pages.append(page)
                if len(r)>15:
                    r=list(r)[:15]
                #print(r)
                for i in r:
                    pages.append(page.goto(i))
            case 'continue_personal':
                r=page.get_all_links()#personal_means_all_links
                all_pages.append(page)
                if len(r)>15:
                    r=list(r)[:15]
                for i in r:
                    pages.append(page.goto(i))
            case 'single_req':
                page.fetch(req=True)#fetch it only,req means requests
                all_pages.append(page)
            case 'single':
                page.fetch()
                all_pages.append(page)
            case _:
                #print(f'Got {rule} as rule.')
                r = page.head()
                if r.status_code>=400:
                    #print(f"{r.status_code} skipping")
                    continue
                if r.url != page.url:#redirected file found
                    page.url=r.url
                    pages.append(page)
                    continue
                print('No rule defined for :', page.url, 'ref:', page.get_last_history())#must not reach here...
                #even more so while running parallel
                print("-----------------------------------------------")
                print(f"Status code: {r.status_code}")
                for key, value in r.headers.items():
                    print(f"{key}: {value}")
                print("-----------------------------------------------")
                exit()
    return all_pages