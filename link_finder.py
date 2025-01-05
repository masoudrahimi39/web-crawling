from html.parser import HTMLParser
from urllib import parse


class LinkFinder(HTMLParser):
    ''' we feed in th html of any page and it saved all the links in the links attribute'''
    def __init__(self, base_url, page_url):
        super().__init__() 
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()


    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        if tag == 'a':      # if it is a link
            for (attributes, value) in attrs: 
                if attributes == 'href':   # if the attribute is a link
                    # adding base_url to the the page_url if is it relative url, otherwise the urljoin method would pass
                    url = parse.urljoin(self.base_url, value)  
                    self.links.add(url)
    
    def page_links(self):
        return self.links 

         

# finder = LinkFinder()

