#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import subprocess

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them

# Returns a list of all files with a special path
def get_special_paths(dir):
  files = os.listdir(dir)
  ret = []
  for file_name in files:
    is_special = re.match('\w*__\w+__.?\w*', file_name)
    if is_special:
      file_path = os.path.abspath(os.path.join(dir, file_name))
      ret.append(file_path)
  return ret

def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  # +++your code here+++
  # Call your functions

  all_files = [];

  for folder in args:
    paths = get_special_paths(folder)
    if todir != '':
      if not os.path.exists(todir):
        os.mkdir(todir)
      for file_path in paths:
        shutil.copy(file_path, os.path.abspath(todir))
    elif tozip != '':
      # Zip things
      all_files.append(paths)

  if tozip != '':
    # Zip things
    zip_cmd = ['zip', '-j', tozip]
    for path in paths:
      zip_cmd.append(path)
    print 'Executing > %s' % zip_cmd
    try:
      output = subprocess.check_output(zip_cmd)
      print 'Output: ' + output
    except subprocess.CalledProcessError:
      print 'Error creating zip file'

if __name__ == "__main__":
  main()
