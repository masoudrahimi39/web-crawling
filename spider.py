from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils import *
import time
import re

class Spider:
    ''' it gets a link and grap the html of the page and then feed the html to linkfinder and move the link from 
    waiting list to crawled list'''

    # class variables (shared among all instances)
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()
    driver = None
    chromedriver_path = ''
    # targeted_info = {
    #     'phd_admission': set(),
    #     'departments': set(),
    #     'faculty': set(), 
    #     'admission_requirement':set(),
    # }

    def __init__(self, project_name, base_url, domain_name, chromedriver_path):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name 
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.chromedriver_path = chromedriver_path
        self.boot()
        self.crawl_page('First Spider', Spider.base_url)


    @staticmethod       # since in this method we are using only class variable, it can be a staticmethod
    def boot( ):
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)
        Spider.setup_driver()

    @staticmethod
    def setup_driver():
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Run in headless mode (optional)
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(Spider.chromedriver_path)
        Spider.driver = webdriver.Chrome(service=service, options=chrome_options)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' crawling ' + page_url)
            print(f'Queue {str(len(Spider.queue))} | crawled {str(len(Spider.crawled))}')
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()
            # Spider.extract_targeted_info(page_url)

    @staticmethod
    def gather_links(page_url):
        try:
            Spider.driver.get(page_url)
            time.sleep(2)
            WebDriverWait(Spider.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            soup = BeautifulSoup(Spider.driver.page_source, 'html.parser')
            links = set(
                urljoin(page_url, a['href']) for a in soup.find_all('a', href=True)
                if urljoin(page_url, a['href']).startswith(base_url)  # Ensure it's within the base URL
            )

            return links
        except Exception as e:
            print(f'Error gathering links from {page_url}: {e}')
            return set()

    
    @staticmethod
    def add_links_to_queue(links):
        # print('linls: ', links)
        for url in links:
            # if the url is present in th queue or crawled list, so it does noting and continure
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            if Spider.domain_name not in url:  
                # do not crawl if the url is a link to a page out of the base_url
                continue
            Spider.queue.add(url)

    # @staticmethod
    # def is_relevant_link(url):
    #     relevant_keywords = ['phd admiision', 'doctoral admiission', 'graduate admission',
    #                           'graduate', 'admission',  'department', 'faculty', 'professor', ]
    #     return any(keyword in url.lower() for keyword in relevant_keywords)


    # @staticmethod
    # def extract_targeted_info(page_url):
    #     try:
    #         soup = BeautifulSoup(Spider.driver.page_source, 'html.parser')
    #         text = soup.get_text().lower()
    
    #         if re.search(r'phd|doctoral', text):
    #             if re.search(r'admission|application|deadline', text):
    #                 Spider.targeted_info['phd_admission'].add(page_url)
    #         if re.search(r'department|school of|faculty of', text):
    #             Spider.targeted_info['departments'].add(page_url)
    #         if re.search(r'faculty|professor|staff', text):
    #             Spider.targeted_info['faculty'].add(page_url)
    #         if re.search(r'admission requirement', text):
    #             Spider.targeted_info['admission_requirement'].add(page_url)

    #     except Exception as e:
    #         print(f'Error extracting info from {page_url}: {e}')

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
        
        for key, value in Spider.targeted_info.items():
            if len(value)>0:
                # print('key, valeu in update_files: ', key, value)
                set_to_file(Spider.project_name + f'/{key}.txt', value)
    
    @staticmethod
    def close_spider():
        if Spider.driver:
            Spider.driver.quit()
            
