Google search Download Script
========================

About
-----
Goes through google search results and tries to find downloadable links with the chosen file format and downloads them into a folder. This script is ideal for downloading ebooks

Dependencies
------------

  * Python 2.7
  * BeautifulSoup (``pip install beautifulsoup4``)
  * google (``pip install google``)
  * fileDownloader.py (``pip install fileDownloader.py``)

Tested on Ubuntu Linux and Windows. It should work on any Linux, OS X, or Windows machine as long as the dependencies are installed. However, sometimes Windows antivirus may create issues when running the script.

Usage
-----

Mandatory argument:
  -t, --term  <search term>
  -f, --format <File format to download>

 Optional Arguments:
   -n, --number <number of google search results to go through>

To download an entire series:

    ~ $ python google_search_dl.py -t SEARCH_TERM -f FILE_FORMAT -n NUMBER_OF_RESULTS

Examples
--------
Download Oregairu light novel epub ebooks

    ~ $ python ebooksearcher.py -t 'oregairu archive.org' -f epub -n 10

Notes
-----
Too many frequent searches might get you banned temporarily. This ban exists for a few hours.
