#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

def custom_sort_key(url):
  matches = re.search(r'-\w+-(\w+).jpg', url)
  if matches:
    return matches.group(1)
  else:
    return url

def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""

  base_url = filename[filename.index('_')+1:]

  ret = []
  f = open(filename, 'r')
  # Read all lines
  logs = f.read()

  url_matches = re.findall('GET\s(\S+)\sHTTP/', logs)

  urls = {}

  for url in url_matches:
    if url not in urls:
      urls[url] = 0
    urls[url] += 1

  for url in sorted(urls.keys(), key=custom_sort_key):
    if  "puzzle" in url and urls[url] > 1:
      ret.append('http://' + base_url + url)

  print '\n'.join(ret)
  return ret;


def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  if not os.path.exists(dest_dir):
    os.mkdir(dest_dir)

  count = 0

  for img in img_urls:
    ufile = urllib.urlopen(img)
    info = ufile.info()
    if "image" in info.gettype():
      text = ufile.read()
      f = open('img' + str(count) + '.jpg', 'w')
      f.write(text)
      f.close()
      print "Image #%d downloaded" % count
      count += 1

  index_file = open('index.html', 'w')

  # Create the HTML string for each image
  all_imgs = '"><img src="'.join('img' + str(x) + '.jpg' for x in range(count))
  all_imgs = '<img src="' + all_imgs + '">'

  index_file.write("""
    <html>
    <body>
    %s
    </body>
    </html>

  """ % all_imgs)


def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
