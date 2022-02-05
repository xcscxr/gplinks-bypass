import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


url = "" # eg: https://gplinks.co/XXXX

# ==============================================

def gplinks_bypass(url):
    client = requests.Session()
    res = client.get(url)
    
    h = { "referer": res.url }
    res = client.get(url, headers=h)
    
    bs4 = BeautifulSoup(res.content, 'lxml')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }

    h = {
        'content-type': 'application/x-www-form-urlencoded',
        'x-requested-with': 'XMLHttpRequest'
    }
    
    time.sleep(10) # !important
    
    p = urlparse(url)
    final_url = f'{p.scheme}://{p.netloc}/links/go'
    res = client.post(final_url, data=data, headers=h).json()

    return res

# ==============================================

print(gplinks_bypass(url))

# ==============================================

'''
SAMPLE OUTPUT:
{
    'status': 'success', 
    'message': 'XXXXXX', 
    'url': 'XXXX' (Bypassed URL)
}
'''
