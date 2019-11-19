#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import requests
import codecs
import urllib
from pandas import Series, DataFrame, concat
import pandas as pd
import numpy as np
from selenium import webdriver
from urllib.request import Request,urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup


if os.path.exists('lt.csv'):
    os.remove('lt.csv')
if os.path.exists('lr.csv'):
    os.remove('lr.csv')
if os.path.exists('la.csv'):
    os.remove('la.csv')
if os.path.exists('lh.csv'):
    os.remove('lh.csv')
if os.path.exists('lz.csv'):
    os.remove('lz.csv')

picpath = 'pic/'
if not os.path.exists(picpath):
    os.makedirs(picpath)


A = "//*[@id=\"content\"]/div/div[1]/div[2]/table/tbody/tr["
B = "]/td[1]"
C = A+"*"+B
D ="//*[@id=\"content\"]/div/div[1]/div[2]/table/tbody/tr["
E = "]/td[2]"
F = D+"*"+E
G = "//*[@id=\"content\"]/div/div[1]/div[2]/table/tbody/tr["
H = "]/td[3]"
I = G+"*"+H
J = "//*[@id=\"content\"]/div/div[1]/div[1]/div[2]"
L = "//*[@id=\"link-report\"]/div/div/div"
M = "div/img"
N = L+"*"+M
#N = L+"*"+M
#M = "//*[@id=\"content\"]/div/div[1]/div[3]/span[4]/a"


print("开始爬取...")
url = 'https://www.douban.com/group/653983/discussion?start=0'
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(2)

titles = driver.find_elements_by_xpath(C)
authors = driver.find_elements_by_xpath(F)
reply = driver.find_elements_by_xpath(I)

print("获得H...")
urls = driver.find_elements_by_xpath("//a")
for url in urls:
    href = url.get_attribute("href")
    lhref = [href]
    lhref = str(lhref)
    res = re.search('https://www.douban.com/group/topic/(.*?)/', lhref)
    if res != None:
        res = res.group()
    else:
        res =res
    res = [res]
    res = pd.DataFrame(res).dropna()
    res.to_csv('lh.csv', mode='a', encoding="'utf-8-sig'", header=False)

print("获得T A R...")
i = 1
while i < 26:
    t_txt = titles[i].text
    a_txt = authors[i].text
    r_txt = reply[i].text
    lt = [t_txt]
    la = [a_txt]
    lr = [r_txt]
    lt = pd.DataFrame(lt)
    la = pd.DataFrame(la)
    lr = pd.DataFrame(lr)
    lt.to_csv('lt.csv', mode='a', encoding="'utf-8-sig'", header=False)
    la.to_csv('la.csv', mode='a', encoding="'utf-8-sig'", header=False)
    lr.to_csv('lr.csv', mode='a', encoding="'utf-8-sig'", header=False)
    i += 1

print("获得Z和I...")
lh_csv = pd.read_csv('lh.csv', low_memory=False, header=None)
i = 0

while i < 25:
    print(i,end=',')
    urllist = lh_csv.iat[i, 1]
    driver.get(urllist)
    driver.implicitly_wait(2)
    zhulou = driver.find_elements_by_xpath(J)
    lzs = zhulou[0].get_attribute('textContent')
    lz = [lzs]
    lz = pd.DataFrame(lz)
    lz = lz.replace('\s+', ' ', regex=True)
    lz.to_csv('lz.csv', mode='a', encoding="'utf-8-sig'", header=False)
    time.sleep(3)
    i += 1
    for pic in driver.find_elements_by_tag_name("img"):
        src = pic.get_attribute("src")
        lsrc = [src]
        lsrc = str(src)
        pp = re.search('(.*)(.webp)', lsrc)
        if pp != None:
            pp = pp.group()
            #pp= [pp]
            #pp = pd.DataFrame(pp).dropna()
            fname = pp.split('/')[-1]
            urllib.request.urlretrieve(pp, fname)
            time.sleep(1)
            #pp.to_csv('li.csv', mode='a', encoding="'utf-8-sig'", header=False)



print("生成结果...")
lt_csv = pd.read_csv('lt.csv', low_memory=False)
la_csv = pd.read_csv('la.csv', low_memory=False)
lr_csv = pd.read_csv('lr.csv', low_memory=False)
lz_csv = pd.read_csv('lz.csv', low_memory=False)
lt_csv.columns = ['no.', 't']
la_csv.columns = ['no.', 'a']
lr_csv.columns = ['no.', 'r']
lz_csv.columns = ['no.', 'z']


if os.path.exists('caizu.csv'):
    os.remove('caizu.csv')
caizu = DataFrame({
    'titles': [],
    'authors': [],
    'reply': [],
    'louzhu': []})
caizu['titles'] = lt_csv['t']
caizu['authors'] = la_csv['a']
caizu['reply'] = lr_csv['r']
caizu['louzhu'] = lz_csv['z']
caizu.to_csv('caizu.csv', mode='a', encoding="'utf-8-sig'", index=None)


driver.refresh()
driver.close()
driver.quit()
print("第一页爬取完毕。")
