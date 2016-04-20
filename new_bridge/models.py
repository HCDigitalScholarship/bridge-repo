# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = True` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from treebeard.mp_tree import MP_Node

class TextStructureNode(MP_Node):
    text_name = models.CharField(max_length=52, blank=True)
    subsection_level = models.SmallIntegerField(blank=False)
    subsection_id = models.CharField(max_length=6, blank=False)
    least_mindiv = models.IntegerField(blank=False)

    node_order_by = ['least_mindiv']
    def __unicode__(self):
        #Climb tree to find parent location information:
        loc_string = ""
        parent = self      
        while not parent.is_root():
            loc_string =unicode(parent.subsection_id) + '.' + loc_string
            parent = parent.get_parent()
        text_name = parent.text_name
        #Descend tree to find child location information:
        child = self
        while not child.is_leaf():
            child = child.get_last_child()
            loc_string += '.'+'x'
        return text_name + '\t' + loc_string

class TextStructureGlossary(models.Model):
    text_name = models.CharField(max_length=52, blank=False)
    subsection_level = models.SmallIntegerField(blank=False)
    subsection_name = models.CharField(max_length=20, blank=True)
    def __unicode__(self):
        s = 'TEXT:\t'+self.text_name
        s += '\nSUBSECTION LVL:\t'+self.subsection_level
        s += '\nSUBSECTION NAME:\t'+self.subsection_name
        return s

class WordAppearencesLatin(models.Model):
    text_name = models.CharField(max_length=52, blank=False)
    word = models.ForeignKey('WordPropertyLatin', blank=False,null=True)
    mindiv = models.SmallIntegerField(blank=False)
    def __unicode__(self):
        s = 'TEXT:\t'+self.text_name
        s += '\nWORD ID:\t'+self.word_id
        s += '\nLOCATION:\t'+self.mindiv
        return s

class WordAppearencesGreek(models.Model):
    text_name = models.CharField(max_length=52, blank=False)
    word = models.ForeignKey('WordPropertyGreek', blank=False,null=True)
    mindiv = models.SmallIntegerField(blank=False)
    def __unicode__(self):
        s = 'TEXT:\t'+self.text_name
        s += '\nWORD ID:\t'+self.word_id
        s += '\nLOCATION:\t'+self.mindiv
        return s

class TextMetadata(models.Model):
    name_for_humans = models.CharField(max_length=100, blank=False)
    name_for_computers = models.CharField(max_length=100, blank=False)
    language = models.CharField(max_length=10, blank=False)
    def __unicode__(self):
        return self.name_for_humans

class WordPropertyLatin(models.Model):
    title = models.CharField(max_length=30, blank=True) 
    display_lemma = models.CharField(max_length=84, blank=True) 
    display_lemma_macronless = models.CharField(max_length=83, blank=True) 
    english_core = models.CharField(max_length=155, blank=True) 
    english_extended = models.CharField(max_length=247, blank=True) 
    lnm_definition = models.CharField(max_length=74, blank=True) 
    aeneid_definition = models.CharField(max_length=1168, blank=True) 
    catullus_definition = models.CharField(max_length=245, blank=True) 
    decl = models.CharField(db_column='decl', max_length=1, blank=True) 
    conj = models.CharField(db_column='conj', max_length=1, blank=True) 
    reg_adj_adv = models.CharField(max_length=1, blank=True) 
    proper = models.CharField(max_length=1, blank=True) 
    part_of_speech = models.CharField(max_length=24, blank=True) 
    dcc_frequency_group = models.CharField(max_length=2, blank=True) 
    dcc_semantic_group = models.CharField(max_length=34, blank=True) 
    def __unicode__(self):
        return self.title

class WordPropertyGreek(models.Model):
    title = models.CharField(max_length=43, blank=True, null=True) 
    accented_lemma = models.CharField(max_length=50, blank=True, null=True) 
    search_lemma = models.CharField(max_length=43, blank=True, null=True) 
    display_lemma = models.CharField(max_length=175, blank=True, null=True) 
    english_definition = models.CharField(max_length=135, blank=True, null=True) 
    questions = models.IntegerField(blank=True, null=True) 
    decl = models.CharField(max_length=4, blank=True, null=True) 
    idiom = models.IntegerField(blank=True, null=True) 
    reg_adject_adv_form = models.IntegerField(blank=True, null=True) 
    proper = models.IntegerField(blank=True, null=True) 
    part_of_speech = models.CharField(max_length=24, blank=True, null=True) 
    exclude_1_0 = models.IntegerField(blank=True, null=True) 
    notes = models.CharField(max_length=34, blank=True, null=True) 
    dcc_semantic_group = models.CharField(max_length=34, blank=True, null=True) 
    def __unicode__(self):
        return self.title

class BookTitlesGreek(models.Model):
    title_of_book = models.TextField(db_column='Title of Book') 
    def __unicode__(self):
        return self.title_of_book
    class Meta:
        managed = True
        db_table = 'book_titles_greek'
'''
class BookTable(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(db_column='Title', max_length=30, blank=True) 
    appearences = models.CharField(db_column='Appearences', max_length=17360, blank=True) 
    field_book_text = models.CharField(db_column='BookText', max_length=52, blank=True) 
    def __unicode__(self):
        return self.title
    class Meta:
        managed = True
        db_table = 'book_table'
'''
class BookTitles(models.Model):
    title_of_book = models.TextField(db_column='Title of Book') 
    def __unicode__(self):
        return self.title_of_book
    class Meta:
        managed = True
        db_table = 'book_titles'
'''
class BookTableGreek(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(db_column='Title', max_length=43, blank=True) 
    appearences = models.CharField(db_column='Appearences', max_length=8, blank=True) 
    field_book_text = models.CharField(db_column=' Book/Text', max_length=44, blank=True) 
    def __unicode__(self):
        return self.title
    class Meta:
        managed = True
        db_table = 'book_table_greek'
'''
