#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import requests
import urlparse

from bs4 import BeautifulSoup
from argparse import ArgumentParser
from socket import gaierror


UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
BLOCKCHAIN = 'https://blockchain.info/address'

email_re = re.compile(r'([\w\.,]+@[\w\.,]+\.\w+)')
link_re = re.compile(r'href="(.*?)"')

def error_handler(msg):

    print '[!]', msg
    sys.exit(1)

def crawl(url, maxlevel):

    # Limit the recursion
    if maxlevel == 0:
        return []

    # Get the webpage
    response = requests.get(url)
    result = []

    # Check if successful
    if response.status_code != 200:
        return []

    # Find and follow all the links
    for link in link_re.findall(response.text):

        # Get an absolute URL for a link
        link = urlparse.urljoin(url, link)
        result += crawl(link, maxlevel - 1)

    # Find all emails on current page
    result += email_re.findall(response.text)
    return result

def set_configs():

    parser = ArgumentParser()

    parser.add_argument('--domain',
                    dest='domain',
                    required=True,
                    type=str,
                    help='The domain from which to grab bitcoin addresses.')

    args = parser.parse_args()

    return {

        'url' : 'http://%s' %\
            (re.sub('http[s]?://', '', args.domain).rstrip('/')),
        'headers' :  {
            'User-Agent' : UA,
        },
    }


def main():

    configs = set_configs()
    try:
        response = requests.get(configs['url'], configs['headers'])
    except gaierror:
        error_handler('Aw shucks.')

    soup = BeautifulSoup(response.content)

    findbit = soup(text=re.compile('[13][a-km-zA-HJ-NP-Z1-9]{25,34}'))

    print '\n'+configs['url']

    for addr in findbit:

        print '[*]Bitcoin Found ---> '+addr

        transaction = '/'.join([BLOCKCHAIN, addr])

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

    emails = crawl(configs['url'], 1)
    print configs['url']
    print "Emails Found::"
    
    for e in emails:
        print e

if __name__ == '__main__':
    main()
