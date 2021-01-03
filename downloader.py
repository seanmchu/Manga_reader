import cloudscraper as cs  
import time, os, sys, re, json, html

scraper = cs.create_scraper()
path = input() 
r = scraper.get(path)
m = json.loads(r.text)
print(m)