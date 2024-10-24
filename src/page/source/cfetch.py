import requests
import logging
import hashlib,os
from ...config import getConfig

config = getConfig()

playwright = None
browser = None

def start_browser():
    global playwright, browser
    if browser:
        return
    logging.debug("Starting playwright browser")
    if not playwright:
        from playwright.sync_api import sync_playwright
        playwright = sync_playwright().start()
    chromium = playwright.chromium
    browser = chromium.launch(channel="chrome")

def shutdown_browser():
    global playwright, browser
    if not browser:
        return
    logging.debug("Stopping playwright browser")
    browser.close()
    #playwright.stop()

#Fetch with added save to file features
class CFetch:
    def __init__(self,url):
        self.url = url
        self.__headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    def playwright_getpage(self):
        return browser.new_page()
    
    def playwright_fetch(self):
        with self.playwright_getpage() as page:
            page.goto(self.url)
            c=page.content().encode()
        return c

    def head(self):
        response = requests.head(self.url, headers=self.__headers, allow_redirects=True)
        return response
    
    def requests_fetch(self):
        response = requests.get(self.url, headers=self.__headers)
        return response.content

    def fetch(self,req=False):
        global browser
        hash = hashlib.md5(self.url.encode()).hexdigest()
        file_path = os.path.join(config['directories']['DOWNLOAD_PATH'], hash)
        logging.debug(f"Url requested: {self.url}")
        if os.path.exists(file_path):
            # File exists, open in read mode ('r')
            logging.debug(f"Found on file: {file_path}")
            with open(file_path, 'rb') as file:
                content = file.read()
                return content
        else:
            logging.debug(f"Cached to new file: {file_path}")
            if req or (not browser):
                response = self.requests_fetch()
                with open(file_path, 'wb') as file:
                    file.write(response)
            else:
                try:
                    #print("Used play", self.url)
                    response = self.playwright_fetch()
                    with open(file_path, 'w') as file:
                        file.write(response)
                except: 
                    print("Used fetch for fallback", self.url)
                    response = self.requests_fetch()
                    with open(file_path, 'wb') as file:
                        file.write(response)
            return response
