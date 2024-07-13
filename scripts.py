#!/usr/bin/env python
from bs4 import BeautifulSoup
import requests
import sys

domain=sys.argv[1]
print(f"Checking: {domain}")

response = requests.get(domain)
doc = BeautifulSoup(response.text, features="html.parser")

links = doc.find_all('script', {"src": True})
for link in links:
    if link['src'].startswith(domain) == False:
        print(link['src'])
