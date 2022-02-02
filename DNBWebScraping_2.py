#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import time
import datetime
import pandas as pd
import csv


# In[3]:


URL = "https://www.certipedia.com/search/certified_companies?locale=en"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}


# In[ ]:


response= requests.get(URL)
for i in range(1,100):
    page = requests.get("https://www.certipedia.com/companies/"+str(i)+"system_certificates?locale=en") 
    soup = BeautifulSoup(page.content,'html.parser')
    tags= soup.find_all(class_='certificate_links')
    for j in tags:
        if j.find(class_='odd'):
            k= soup.find(h1.string.strip(:)[1])
            url = "https://www.certipedia.com/quality_marks/"+str(k)+"?locale=en&certificate_number=39+00+0591803"
            df= soup.find(id='container').get_text()

df.to_csv('project_2.csv')
    

