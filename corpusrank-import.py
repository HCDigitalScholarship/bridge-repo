#A script for importing the tsv file for corpus ranks to the django database.
#import csv, sys, os
import sys,os 
sys.path.append("new_bridge")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from new_bridge.models import * #django
#django.setup()
#from new_bridge/models.py import *
import csv
import django
django.setup()
from itertools import chain 
dataReader = csv.reader(open("bridge-cr.tsv"), delimiter='\t', quotechar='"')
accu = 0

greek_words = WordPropertyGreek.objects.all()
latin_words = WordPropertyLatin.objects.all()
greek_worda = WordAppearencesGreek.objects.all()


#for n in range(50):
#    print "Greek word " 
 #   print greek_words[n].title
  #  print "Latin word "
   # print latin_words[n].title


collection = []
#collection.append(latin_words.get(title="ET/2"))
#collection.append(greek_words.get(title="ET/2"))
#print collection
for row in dataReader:
   if row[0] != 'title':
       if accu > 20:
          break
       else:
          greek_filter = greek_words.filter(title=row[0])
          latin_filter = latin_words.filter(title=row[0])
          
          if latin_filter.count() > 0:
             collection.append(latin_filter)
          #else:
           #  update = latin_words.get(title=row[0])
            # collection.append(update)

print collection
print len(collection)
          #collection.append(greek_words.get(id=73))
          #update = greek_words.get(title=row[0])
          #collection.append(update)




#for row in dataReader:
    #if row[0] != 'title':
       #accu+=1
       #update = all_words.get(title=row[0])
       #accu+=1
       #if accu < 50:
          #print row

