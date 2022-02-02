#!/usr/bin/env python
# coding: utf-8

# In[3]:


from bs4 import BeautifulSoup
import requests
import time
import datetime
import pandas as pd
import csv


# In[2]:


URL = "https://www.epa.gov/greenpower/green-power-partnership-national-top-100"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

page = requests.get(URL, headers=headers)

soup1 = BeautifulSoup(page.content, "html.parser")

soup2 = BeautifulSoup(soup1.prettify(), "html.parser")


# In[9]:


table = soup2.find(class_='tablebord')


# In[ ]:


base_url = 'https://www.epa.gov/greenpower/meet-our-partners?partner='
all_urls = ['https://www.epa.gov/greenpower/meet-our-partners?partner=googlellc']
current_page= URL

response= requests.get(current_page)

while response.status_code==200:
    soup= BeautifulSoup(response.text,'html.parser')
    next_page= soup.find(a['href'])
    if next_page is None:
        break
    next_page_url= base_url + next_page.a['href']
    all_urls.append(next_page_url)
    current_page= next_page_url
    response= requests.get(current_page)
    for i in soup.find_all(target_='_blank'):
        df= i

df.to_csv('project_1.csv')


# In[ ]:




