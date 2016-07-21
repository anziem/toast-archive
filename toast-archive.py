#!/usr/bin/env python

"""Script to create an archive of website The-Toast.net. Must be executed with python 3 to
parse non-ascii unicode characters in strings. Otherwise uncomment python 2 lines to convert quotation characters and ignore the rest."""

from bs4 import BeautifulSoup
import os.path
import requests
import re

out_file = open('toast-archive-test.tsv', 'w')
header = '\t'.join(['Date Published', 'Title', 'Author 1', 'Author 2', 'Series', 'Link', '\n'])
out_file.write(header)

def getPage(url):
    c = ''
    print("Fetching the data via the URL, %s." % (url))
    headers = {'user-agent': 'Mozilla/47.0.1'}
    result = requests.get(url, headers = headers)
    c = result.content
    c = BeautifulSoup(c, "html.parser")
    return c

for i in range(1, 372):  # site is closed, so can hardcode the total number of pages
    html = getPage('http://the-toast.net/page/%s' % i)
    teasers = html.find_all('div', class_=re.compile("teaser.*teaser-post"))

    for post in teasers:
        date_block = post.find(datetime=True)
        if date_block:  # some posts are missing dates
            date = date_block.get('datetime')
        else:
            link = post.find('a', href=re.compile('http://the-toast.net/\d+')).get('href')
            date_pattern = re.compile('\d{4}/\d{2}/\d{2}')
            date = date_pattern.search(link).group()
        # necessary for python 2 - must convert unicode to ascii
#         title_utf = post.find('h2').find_next('a').get_text().strip()
#         title_utf = title_utf.replace(u"\u2018", "\'").replace(u"\u2019", "\'").replace(u"\u201c",'\"').replace(u"\u201d", '\"')
#         title = title_utf.encode('ascii', 'ignore')
        # comment next line out if using python 2
        title = post.find('h2').find_next('a').get_text().strip()
        row = '\t'.join([date, str(title)])
        author_block = post.find('h3')
        if author_block:  # some posts are missing authors
            authors_link = author_block.find_next('a')
            authors_str = authors_link.get_text()
            authors_list = authors_str.split(' & ')
            if len(authors_list) == 1:
                authors_list = authors_list[0].split(' and ')
        else:
            authors_list = [""]
        for author in authors_list:
            row = '\t'.join([row, author])
        if len(authors_list) == 1:  # need to leave space for second author
            row += '\t'
        # necessary for python 2 - must convert unicode to ascii
#         series_utf = post.find('span', class_="article-from").find_next('a').get_text()
#         series_utf = series_utf.replace(u"\u2018", "\'").replace(u"\u2019", "\'").replace(u"\u201c",'\"').replace(u"\u201d", '\"')
#         series = series_utf.encode('ascii', 'ignore')
        # comment next line out if using python 2
        series_block = post.find('span', class_="article-from")
        if series_block:
            series = series_block.find_next('a').get_text()
        else:  # some posts are missing series block
            series = 'n/a'
        link = post.find('a', href=re.compile('http://the-toast.net/\d+')).get('href')
        row = '\t'.join([row, series, link, '\n'])
#         print(row)  # debugging
        out_file.write(row)
