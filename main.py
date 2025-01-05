import threading 
from queue import Queue
from spider import Spider
from domain import *
from utils import *

CHROMEDRIVER_PATH = r'C:\Users\masou\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'
PROJECT_NAME = 'book_crawling'
HOME_PAGE = 'https://books.toscrape.com/'
DOMAIN_NAME = get_domain_name(HOME_PAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 4
queue = Queue()

spider = Spider(PROJECT_NAME, HOME_PAGE, DOMAIN_NAME, CHROMEDRIVER_PATH)


# create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done() 


# each queue link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# check if there items it the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(f'{str(len(queued_links))} links in the queue')
        create_jobs()
         
try:
    create_workers()
    crawl()
finally:
    Spider.close_spider() 
