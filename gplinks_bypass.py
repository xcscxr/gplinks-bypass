

import time
import cloudscraper
from bs4 import BeautifulSoup

import requests
# eg: https://gplinks.co/XXXX
url = "https://gplinks.co/Z94r6"

# =======================================

def gplinks_bypass(url: str):
 client = cloudscraper.create_scraper(allow_brotli=False)  
 domain ="https://gplinks.co/"
 referer = "https://mynewsmedia.co/"

 vid = client.get(url, allow_redirects= False).headers["Location"].split("=")[-1]
 url = f"{url}/?{vid}"

 response = client.get(url, allow_redirects=False)
 soup = BeautifulSoup(response.content, "html.parser")
    
    
 inputs = soup.find(id="go-link").find_all(name="input")
 data = { input.get('name'): input.get('value') for input in inputs }
    
 time.sleep(10)
 headers={"x-requested-with": "XMLHttpRequest"}
 bypassed_url = client.post(domain+"links/go", data=data, headers=headers).json()["url"]
 return bypassed_url

print(gplinks_bypass(url))
