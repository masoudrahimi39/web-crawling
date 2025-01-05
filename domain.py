from urllib.parse import urlparse


# get damain name
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return f'{results[-2]}.{results[-1]}'
    except :
        return '' 
    
# get sub domain in name (mail.name.example.com)
def get_sub_domain_name(url):
    try:   
        return urlparse(url).netloc
    except:
        return ''
