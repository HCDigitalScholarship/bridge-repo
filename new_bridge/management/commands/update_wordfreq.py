#A script for updating the word frequencies of each word.

from django.core.management.base import BaseCommand, CommandError
from new_bridge.models import *
import sys
import os
import mysql.connector


class Command(BaseCommand):
    help = "Run this command to update the word_frequency field of all entries in the database."
    def handle(self, *args, **options):
           print "BEGINNING UPDATE WORD FREQUENCIES SCRIPT"
             #Change this for various print messages
             #get all the words and iterate over frequencies
           """accu=0
           for gword in WordPropertyGreek.objects.all().iterator():
                accu+=1
                if accu < 10000:
                   print "WORDPROPERTY INFO:\n", gword
                   print "WORD ID IN WORDPROPERTYGREEK", gword.id
                   some_ids = list(WordAppearencesGreek.objects.filter(word__exact=gword.id))
                   print "WORD ID AS ATTAINED IN WORDAPPEARENCES", some_ids[0].word
                   print "SECOND WORD ID IN WORDAPPEARENCES", some_ids[1].word
                   print "COUNT", len(some_ids)
                   gword.word_frequency = WordAppearencesGreek.objects.filter(word__exact=gword.id).count()
                   print "WORD FREQUENCY FOR ITER " + str(accu) + ": " + str(gword.word_frequency)
                else:
                   print finished.
                 break
                #gword.word_freq = WordAppearencesGreek.filter(word__exact=gword.id).count()
              #gword.save()
           print "UPDATING ALL GREEK WORD'S (WORDPROPERTYGREEK) word_frequency FIELD"
           """

           """accu=0
           mult=1
           for gword in WordPropertyGreek.objects.all().iterator():
               accu+=1
               if accu < 1000:
                  continue
               elif accu == 1000 or accu < 4000:
                  if accu < mult*20:
                     gword.word_frequency = WordAppearencesGreek.objects.filter(word__exact=gword.id).count()
                     print gword.word_frequency
                     gword.save()
                  else:
                    print "Iteration: ", accu
                    mult+=1
                    gword.word_frequency = WordAppearencesGreek.objects.filter(word__exact=gword.id).count()
                    print gword.word_frequency
                    gword.save()
               else:
                  break
           print "FINISHED UPDATING " + str(accu-1) + " WORD FREQUENCY\n"""
           """print "UPDATING ALL LATIN WORD'S (WORDPROPERTYLATIN) word_frequency FIELD"
           for lword in WordPropertyLatin.objects.all().iterator():
               lword.word_frequency = WordAppearencesLatin.objects.filter(word__exact=lword.id).count()
               lword.save()

           print "FINISHED UPDATING ALL LATIN WORD'S WORD FREQUENCY\n"
           """

           cnx = mysql.connector.connect(user='root', password='safari77',
                              host='localhost',
                              database='bridge')
           cursor = cnx.cursor(buffered=True)
           query = ("SELECT title, count(title) FROM new_bridge_wordappearencesgreek a JOIN `new_bridge_wordpropertygreek`p on a.word_id = p.`id` GROUP by title ORDER BY count(title) DESC")
           cursor.execute(query)
           for row in cursor:
              title = row[0]
              count = row[1]
              print title, count
              WordAppearencesGreek



           print "SCRIPT DONE."
