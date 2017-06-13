#!/usr/bin/python
# -*- coding: utf-8 -*-

# Lit of libraries needed to run the programme
import threading
import urllib2
import time
import os
import sys
import traceback
import fileDownloader
from bs4 import BeautifulSoup
from google import search
from urlparse import urljoin


def Soup(htm):
    return BeautifulSoup(htm, 'html.parser')


# The following acquires the html source code using urllib2
def gethtml(url):
    time.sleep(2)
    req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
    con = urllib2.urlopen(req)
    html = con.read()
    return html

def search_url (url, folder_name, format):
    ext = '.%s'%(format)
    if ext in url:

        if 'github.com' in url:
            url = url.replace('blob', 'raw')
        try:
            fileDownloader.DownloadFile(url=url,
                                        localFileName=os.path.join(folder_name, url.split('/')[-1])).download()
        except:
            traceback.print_exc()
            return

    else:
        try:
            soup = Soup(gethtml(url))
        except:
            traceback.print_exc()
            return

        for link in soup.find_all('a', href=True):
            href = link['href']
            try:
                if ext in href:
                    if 'http' not in href:
                        href = urljoin(url,href)
                    if 'github.com' in href:
                        href = href.replace('blob', 'raw')
                    print(href)
                    fileDownloader.DownloadFile(url=href,
                                                localFileName=os.path.join(folder_name,href.split('/')[-1])).download()
            except:
                traceback.print_exc()
                continue

# Seaching for each ebook using google and finding for suitable links and downloadingt those found
def ebooksearch(search_term, qnum, format):

    print('Looking for ebook: %s' %(search_term))

    #folder_name = unicode(ebook_name[:150], errors='replace')
    folder_name = search_term[:150]

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    try:
        google_search_results = search(query=search_term, stop=qnum)
    except:
        sys.exit('Google has banned you temporarily!!!')

    searchThreads = []

    for url in google_search_results:
        #search_for_ebooks(ebook_name,url)
        searchThread = threading.Thread(target=search_url, args=(url, folder_name, format))
        searchThreads.append(searchThread)
        searchThread.start()

    # Wait for all threads to end.
    for searchThread in searchThreads:
        searchThread.join()
    print('Done.')


def _Main():
    import argparse
    parser = argparse.ArgumentParser(description='Download files from Google')
    parser.add_argument('--term', '-t', type=str, help='Give search term')
    parser.add_argument('--format', '-f', type=str, help='Give format of files to be downloaded')
    parser.add_argument('--number', '-n', type=int,default=10, help='Number of maximum results')
    args = parser.parse_args()
    ebooksearch(search_term=args.term, format=args.format, qnum=args.number)


# main function which asks for command line arguments
if __name__ == '__main__':
    _Main()
