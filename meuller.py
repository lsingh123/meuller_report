#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 09:43:12 2019

@author: lavanyasingh
"""

# a script to grab links, anchor text, page, and volume # from the NYtimes
# annotated version of the Mueller report

from bs4 import BeautifulSoup
import csv
from selenium import webdriver

def get_soup():
    driver = webdriver.Chrome()
    url = 'https://www.nytimes.com/interactive/2019/04/18/us/politics/mueller-report-document.html'
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return soup

def get_sources():
    #soup = get_soup()
    pages = soup.find_all("div", { "class": 'g-doc-page has-ocr'})
    results = []
    footnotes = []
    for page in pages[8:]:
        pg_num = page.find("p", {"class": "g-doc-page-number"}).get_text()
        paragraphs = page.find_all('p')
        for paragraph in paragraphs:
            links = paragraph.find_all('a')
            if str(paragraph).find('g-footnote') == -1:
                for link in links:
                    if str(link).find('http') != -1:
                        results.append([link.get('href'), link.get_text(), pg_num])
            else:
                fn_num = paragraph.find('sup').get_text()
                for link in links:
                    if str(link).find('http') != -1:
                        footnotes.append([link.get('href'), link.get_text(), pg_num, fn_num])
    return results, footnotes


def get_pg_vol(pgvol):
    pieces = pgvol.split(' ')
    try:
        vol = pieces[1][0:1]
        pg = pieces[3]
    except IndexError as e:
        return 'appendix', pieces[1]
    return vol, pg

def write_sources():
    body, footnotes = get_sources()
    count = 0 
    with open('meuller_body.csv', mode = 'w') as f:
        w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['volume', 'page', 'anchor text', 'link'])
        for link in body:
            count += 1
            print ('body', count)
            vol, pg = get_pg_vol(link[2])
            w.writerow([vol, pg, link[1], link[0]])
    with open('meuller_footnotes.csv', mode = 'w') as f:
        w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['footnote', 'volume', 'page', 'anchor text', 'link'])
        for link in footnotes:
            count += 1
            print('footnote', count)
            vol, pg = get_pg_vol(link[2])
            w.writerow([link[3], vol, pg, link[1], link[0]])

write_sources()
    