import time
import requests
import threading
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

THREADS = 20

# list of URLs
links = [
    'https://gplinks.co/LINK1',
    'https://gplinks.co/LINK2',
    'https://gplinks.co/LINK3',
    # ...
    # ...
]

out_dict = {}
out_dict_l = threading.Lock()
    
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

    with out_dict_l:
        out_dict[url] = res

# ==============================================

def gplinks_bypass_multi(links, threads=5):
    with ThreadPoolExecutor(max_workers=threads) as exe:
        for link in links:
            exe.submit(gplinks_bypass, link)
        return out_dict

# ==============================================

print(gplinks_bypass_multi(links, threads=THREADS))

# ==============================================

'''
SAMPLE OUTPUT:
{
   "https://gplinks.co/LINK1":{
      "status":"success",
      "message":"XXXX",
      "url":"BYPASSED_URL_1"
   },
   "https://gplinks.co/LINK2":{
      "status":"success",
      "message":"XXXX",
      "url":"BYPASSED_URL_2"
   },
   ...
}
'''
