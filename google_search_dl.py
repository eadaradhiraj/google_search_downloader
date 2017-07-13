#!/usr/bin/python
# -*- coding: utf-8 -*-

# Lit of libraries needed to run the programme
import threading
import os
import sys
import traceback
from bs4 import BeautifulSoup
from google import search
from urllib.request import Request, urlopen
from urllib.parse import urljoin

request_headers = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "http://thewebsite.com",
    "Connection": "keep-alive"
}

def download_file(url, out_path):
    u = urlopen(url)
    f = open(out_path, 'wb')
    meta = u.info()
    file_size = int(meta['Content-Length'])
    print ("Downloading: %s Bytes: %s" % (out_path, file_size))

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print(status, end="\r")
    f.close()

# The following acquires the html source code using urllib2
def gethtml(url):
    return urlopen(
        Request(url, headers=request_headers)
    ).read().decode('utf-8')

def search_url (url, folder_name, format):
    ext = '.%s'%(format)
    if ext in url:

        if 'github.com' in url:
            url = url.replace('blob', 'raw')
        try:
            download_file(url=url,
                          out_path=os.path.join(folder_name, url.split('/')[-1]))
        except:
            traceback.print_exc()
            return

    else:
        try:
            soup = BeautifulSoup(gethtml(url), 'html.parser')
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
                    download_file(url=href,
                                  out_path=os.path.join(folder_name,href.split('/')[-1]))
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
