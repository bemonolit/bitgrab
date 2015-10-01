#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import requests
import urlparse
from bs4 import BeautifulSoup


url = 'http://www.top-hat-sec.com'
headers = {                     
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
}
req = requests.get(url, headers)
c = req.content

if req.status_code == 200:
    try:
        print 'Server Responded OK'
    except gaierror:
        print 'Oh No!'
    
soup = BeautifulSoup(c)

#regex for bitcoin

findbit = soup(text=re.compile('[13][a-km-zA-HJ-NP-Z1-9]{25,34}'))
print '\n'+url

for addr in findbit:
    print '[*]Bitcoin Found ---> '+addr
    transaction = 'https://blockchain.info/address/'+addr
    print '[*]Snagging Transaction Data\n'
    reqtrans = requests.get(transaction)    
    b = reqtrans.content
    transoup = BeautifulSoup(b)
    findtrans = transoup(text=re.compile('[13][a-km-zA-HJ-NP-Z1-9]{25,34}'))
    for linkc in findtrans:
        print 'Other Addresses Affiliated With This Address: -->'+linkc

#find all links
for linka in soup.findAll('a', href=True):
    if "http" in linka['href']:
        print linka['href']

#find all onion sites (sort of redundant but we can think of something else later)
for linkb in soup.findAll('a', href=True):
    if ".onion" in linkb['href']:
        print linkb['href']






#The fucking around section (it works tho)

############################################################################################################

#e-mail regexp:

email_re = re.compile(r'([\w\.,]+@[\w\.,]+\.\w+)')

# HTML <a> regexp
# Matches href="" attribute

link_re = re.compile(r'href="(.*?)"')

def crawl(url, maxlevel):
    # Limit the recursion
    if(maxlevel == 0):
        return []

    # Get the webpage
    req = requests.get(url)
    result = []

    # Check if successful
    if(req.status_code != 200):
        return []

    # Find and follow all the links
    links = link_re.findall(req.text)
    for link in links:
        # Get an absolute URL for a link
        link = urlparse.urljoin(url, link)
        result += crawl(link, maxlevel - 1)

    # Find all emails on current page
    result += email_re.findall(req.text)
    return result

emails = crawl(url, 1)
print url
print "Emails Found::"

for e in emails:
    print e
