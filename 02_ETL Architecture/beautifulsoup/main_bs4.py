import requests
#import pandas as pd
from bs4 import BeautifulSoup

url = "https://hdr.undp.org/en/indicators/183506"
req = requests.get(url)

soup = BeautifulSoup(req.content, 'html5lib')
print(soup.prettify())