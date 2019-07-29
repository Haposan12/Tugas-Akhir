#Reducer
from itertools import groupby
from operator import itemgetter
import sys
import requests
import re
from bs4 import BeautifulSoup
import time
reload(sys) 
sys.setdefaultencoding('utf8')
def read_mapper_output(file, separator='\t'):
   for line in file:
      yield line.rstrip().split(separator, 1)
def postag(kata):
   response = requests.get("https://kbbi.kemdikbud.go.id/entri/"+kata)
   soup = BeautifulSoup(response.text, 'html.parser')
   results = soup.find_all('div', attrs={'class': 'container body-content'})
   result = results[0]
   try:
      if (result.find('ol')):
         ol = result.find('ol')
         return ol.li.i.span.text
      elif result.find('i'):
         i = result.find('i')
         return i.text
      else:
         ul = result.find('ul')
         return ul.li.i.span.text
   except:
      return 'Entri tidak ditemukan'
def postagRoot(kata):
   response = requests.get("https://kbbi.kemdikbud.go.id/entri/"+kata)
   soup = BeautifulSoup(response.text, 'html.parser')
   results = soup.find_all('div', attrs={'class': 'container body-content'})
   result = results[0]
   root = result.find('h2')
   if root.find('span', attrs={'class': 'rootword'}):
      hasil = 'ada'
   else:
      hasil = 'ga'
   return hasil
def findRoot(kata):
   response = requests.get("https://kbbi.kemdikbud.go.id/entri/"+kata)
   soup = BeautifulSoup(response.text, 'html.parser')
   results = soup.find_all('div', attrs={'class': 'container body-content'})
   result = results[0]
   if postagRoot(kata) == 'ga' and postag(kata) != 'Entri tidak ditemukan':
      return kata
   else:
      word = result.find('h2')
      if word.find('span'):
         h2 = word.find('span')
         return h2.text
def stem(word): 
   awalan = ["di","ke","se","ter","me","mem","men","meng","meny","pe","pem","pen","peng","peny", "ber","bel","be","per","pel","pe"]
   akhiran = ["i","kan","an","kah","lah","tah","pun","ku","mu","nya"]
   indexAwalan = []
   indexAkhiran = []
   root = []
   hasil = []
   result = []
   result2 = []
   text = open(‘/home/hadoop/Desktop/kamus.txt’, ‘r’)
   kamus = text.read().split()

   if word in kamus :
      return word
   else:
      for i in range(0,5):
         start = word[0:i]
         if start in awalan:
            indexAwalan.append(i)
for i in range(1,4):
l = len(word)
end = word[l-i:l]
if end in akhiran:
indexAkhiran.append(i)
if len(indexAwalan) != 0:
for i in range(0,len(indexAwalan)):
prefix = word[0:indexAwalan[i]]
key = word[indexAwalan[i]:len(word)]
if prefix=="meng" or prefix=="peng":
key1 = "k"+key
root.append(key1)
root.append(key)
elif prefix=="men" or prefix=="pen":
key1 = "t"+key
root.append(key1)
root.append(key)
elif prefix=="meny" or prefix=="peny":
key1 = "s"+key
root.append(key1)
root.append(key)            
elif prefix=="mem" or prefix=="pem":
key1 = "p"+key
root.append(key1)
root.append(key)
else:
key=key
root.append(key)
if len(indexAkhiran) != 0:
for kata in root:
for i in range(0,len(indexAkhiran)):
key = kata[0:len(kata)-indexAkhiran[i]]
hasil.append(key)
else:
hasil = root
if len(indexAkhiran) != 0:
for i in range(0,len(indexAkhiran)):
key = word[0:len(word)-indexAkhiran[i]]
hasil.append(key)
for kata in hasil:
result.append(kata)
for kata in root:
result.append(kata)
indexAkhiran = []
indexAwalan = []
root = []
for kata in result:
for i in range(0,5):
start = word[0:i]
if start in awalan:
indexAwalan.append(i)
if len(indexAwalan) != 0:
for i in range(0,len(indexAwalan)):
prefix = word[0:indexAwalan[i]]
key = word[indexAwalan[i]:len(word)]
if prefix=="meng" or prefix=="peng":
key1 = "k"+key
root.append(key1)
root.append(key)
elif prefix=="men" or prefix=="pen":
key1 = "t"+key
root.append(key1)
root.append(key)
elif prefix=="meny" or prefix=="peny":
key1 = "s"+key
root.append(key)            
elif prefix=="mem" or prefix=="pem":
key1 = "p"+key
root.append(key1)
root.append(key)
else:
key=key
root.append(key)
for kata in root:                                                                                                             
result.append(kata)
result = list(dict.fromkeys(result))
indexAkhiran = []
indexAwalan = []
root = []
for kata in result:
for j in range(0,5):
start = kata[0:j]
if start in awalan:
 indexAwalan.append(start)
indexAwalan = list(dict.fromkeys(indexAwalan))
for kata in result:
if len(indexAwalan) != 0:
for i in range(0,len(indexAwalan)):
root.append(re.sub('^'+indexAwalan[i],'',kata))
root = list(dict.fromkeys(root))
for kata in root:
result.append(kata)
result = list(dict.fromkeys(result))
for kata in result:
if kata in kamus:
return kata    
def main(separator='\t'):
   # input comes from STDIN (standard input)
   data = read_mapper_output(sys.stdin, separator=separator)
   # groupby groups multiple word-count pairs by word,
   # and creates an iterator that returns consecutive keys and their group:
   #   current_word - string containing a word (the key)
   #   group - iterator yielding all ["&lt;current_word&gt;", "&lt;count&gt;"] items
hasil = “”
for current_word, group in groupby(data, itemgetter(0)):
   try:
      total_count = sum(int(count) for current_word, count in group)
      if current_word not in stopword :
      print ("%s%s%s" % (current_word, separator, stem(current_word)))
   except ValueError:
      # count was not a number, so silently discard this item
      pass
if __name__ == "__main__":
   start = time.time()
   main()
end = time.time()
print(end-start)
