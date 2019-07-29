#Mapper
import sys
import re
for line in sys.stdin:
# remove leading and trailing whitespace
line = line.strip()
line = re.sub(r'[^\w\s]','',line).lower()
line = re.sub(r'[0-9]+', '', line)
# split the line into words
words = line.split()
# # increase counters
for word in words:
# write the results to STDOUT (standard output);
# what we output here will be the input for the
# Reduce step, i.e. the input for reducer.py
#
# tab-delimited; the trivial word count is 1
print '%s\t%s' % (word, 1)
