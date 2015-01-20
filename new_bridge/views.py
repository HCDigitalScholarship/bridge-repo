# from new_bridge.models import 'insert class/model names here' 
from django.views import generic
import unicodedata
from new_bridge.models import BookTable, WordTable, BookTitles, BookTableGreek, WordTableGreek, BookTitlesGreek
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response
import json
# defining global variables

# ending definition of global variables

def IndexView(request):
	return render(request, 'index.html')
	
def TextListView(request):
	return render(request, 'textlist.html')

class AboutView(generic.ListView):
	template_name = 'about.html'
	model = BookTable
	
class HelpView(generic.ListView):
	template_name = 'help.html'
	model = BookTable

class ContactView(generic.ListView):
	template_name = 'contact.html'
	model = BookTable

#@csrf_exempt
def book_select(request, language):
	book_list = []
	all_entries = 0
	if language == "Greek":
		all_entries =  BookTitlesGreek.objects.all()
	else:
		all_entries =  BookTitles.objects.all()

	for each in all_entries:
		book_list.append(each.title_of_book)
	results = book_list

	return render(request, 'textlist.html', {"booklist": results, "language": language})


@require_http_methods(["POST"])
def words_page(request, language):
	if language == "Greek":
		return greek_words_page(request, language)
	else:
		return latin_words_page(request, language)

def latin_words_page(request, language):
        if request.method =="POST":
                word_list = []
                word_list2 = []
                final_list = []
                wordcount = 0
                text = request.POST["textlist"]
                bookslist = request.POST.getlist("book")
                text_from = request.POST["text_from"]
                text_to = request.POST["text_to"]
                all_entries = BookTable.objects.all()
		word_table_entries = WordTable.objects.all()
                for each in all_entries: 
                        if text_from == "" and text_to == "" and text == each.field_book_text:
                            word_list.append(each.title)
                        elif text == each.field_book_text:
				if each.field_book_text.strip() == "DCC Latin Core":
                                	word_in_core = each.title
                                	for j in word_table_entries:
                                        	if word_in_core == j.title:
                                                	core_helper( j,j.dcc_frequency_rank, word_list,text_from, text_to)
				else:
                            		appearances = each.appearences
                           		helper(appearances, each, word_list, text_from, text_to)

                        for i in bookslist:
                                if i[0:] == each.field_book_text:
                                        appearances = each.appearences
					if i != "DCC Latin Core": 
						from_sec = request.POST[each.field_book_text + " from"]
						to_sec = request.POST[each.field_book_text + " to"]
						if from_sec == "":
							word_list2.append(each.title)
						else:
							helper(appearances, each, word_list2, from_sec, to_sec)
					else:
						from_sec = request.POST[each.field_book_text + " from"]
                                                to_sec = request.POST[each.field_book_text + " to"]
						if from_sec == "":
							word_list2.append(each.title)
						else:
							word_in_core2 = each.title
        		                                for k in word_table_entries:
	                	                                if word_in_core2 == k.title:
                                		                        core_helper( k, k.dcc_frequency_rank, word_list2, from_sec, to_sec)
		
                for i in word_list:
                        if i not in word_list2:
                                final_list.append(i)
		final_list.sort()
		global_list = final_list[:]
		request.session['global_list'] = global_list
                wordcount = len(final_list)
                actual_words = []
                all_words = WordTable.objects.all()
                for word in final_list:
                        for each in all_words:
                                if word == each.title:
                                        actual_words.append(each)
		if bookslist == []:
			books = "nothing"
	
		elif bookslist != []:
			books = ""
			loop_counter = 1
                        for i in bookslist:
				print loop_counter
                                if len(bookslist) > 1 and loop_counter != len(bookslist):
                                        books = books + i + ", "
					loop_counter+=1
                                else:
                                        books = books + i

		if text_from == "":
			text_from = "all"
		
		elif text_from != "":
			text_from = "from "+text_from
			text_to = "to "+text_to

                return render(request, "words_page.html", {"language": language, "text": text, "text_from": text_from, "text_to": text_to, "books": books, "wordcount":wordcount, "words" : actual_words})


@require_http_methods(["POST"])
def greek_words_page(request, language):
        if request.method =="POST":
                word_list = []
                word_list2 = []
                final_list = []
                wordcount = 0
                text = request.POST["textlist"]
                bookslist = request.POST.getlist("book")
                text_from = request.POST["text_from"]
                text_to = request.POST["text_to"]
                all_entries = BookTableGreek.objects.all()
                word_table_entries = WordTableGreek.objects.all()
                for each in all_entries:
                        if text_from == "" and text_to == "" and text == each.field_book_text:
				word_list.append(each.title)
                        elif text == each.field_book_text:
                                if each.field_book_text.strip() == "DCC Greek Core":
                                        word_in_core = each.title
                                        for j in word_table_entries:
                                                if word_in_core == j.title:
                                                        greek_core_helper( j,j.dcc_core_frequency, word_list,text_from, text_to)
                                elif each.field_book_text.strip() == "Herodotus Book 1 Core (412 words > 10 times)":
					word_in_core = each.title
					for j in word_table_entries:
						if word_in_core == j.title:
							greek_core_helper( j,j.herodotus_1_frequency_rank, word_list,text_from, text_to)	
				elif each.field_book_text.strip() == "Introduction to Ancient Greek (Luschnig)":
					appearances = each.appearences
					greek_helper(appearances, each, word_list, text_from, text_to)
				elif each.field_book_text.strip() == "Reading Greek (JACT)":
					appearances = each.appearences
					greek_helper(appearances, each, word_list, text_from, text_to)
				else:
                                        appearances = each.appearences
                                        helper(appearances, each, word_list, text_from, text_to)

                        for i in bookslist:
                                if i[0:] == each.field_book_text:
                                        appearances = each.appearences
                                        if i != "DCC Greek Core":
                                                from_sec = request.POST[each.field_book_text + " from"]
                                                to_sec = request.POST[each.field_book_text + " to"]
                                                if from_sec == "":
                                                        word_list2.append(each.title)
                                                else:
                                                        helper(appearances, each, word_list2, from_sec, to_sec)
                                        elif i == "DCC Greek Core":
                                                from_sec = request.POST[each.field_book_text + " from"]
                                                to_sec = request.POST[each.field_book_text + " to"]
						if from_sec == "":
                                                        word_list2.append(each.title)
                                                else:
                                                        word_in_core2 = each.title
                                                        for k in word_table_entries:
                                                                if word_in_core2 == k.title:
                                                                        greek_core_helper( k, k.dcc_core_frequency, word_list2, from_sec, to_sec)
					else: # i is Herodotus Core
						from_sec = request.POST[each.field_book_text + " from"]
                                                to_sec = request.POST[each.field_book_text + " to"]
                                                if from_sec == "":
                                                        word_list2.append(each.title)
                                                else:
                                                        word_in_core2 = each.title
                                                        for k in word_table_entries:
                                                                if word_in_core2 == k.title:
                                                                        core_helper( k, k.herodotus_1_frequency_rank, word_list2, from_sec, to_sec)
	


                for i in word_list:
                        if i not in word_list2:
                                final_list.append(i)

		final_list.sort()
		global_list = final_list[:]
		request.session['global_list'] = global_list
                wordcount = len(final_list)
                actual_words = []
                all_words = WordTableGreek.objects.all()
                for word in final_list:
                        for each in all_words:
                                if word == each.title:
                                        actual_words.append(each)
		
		if bookslist == []:
                        books = "nothing"
	
		elif bookslist != []:
                        books = ""
                        for i in bookslist:
                                if len(bookslist) > 1:
                                        books = books + i + ", "
                                else:
                                        books = books + i

			
		if text_from == "":
                        text_from = "all"

                elif text_from != "":
                        text_from = "from "+text_from
                        text_to = "to "+text_to
		
                return render(request, "words_page.html", {"language": language, "text": text, "text_from": text_from, "text_to": text_to, "books": books, "wordcount":wordcount, "words" : actual_words})



# This function turns the appearances into a list of lists, where each appearance is itself a list,
# and each value in the list represents a certain subdivision of a text, like chapter, line, etc. 
def list_of_lists(a):
	# splits individual appearances first by commas
        a = a.split(",")
        b = []
	# then by periods
        for i in a:
                b.append(i.split("."))
	return b

# This function decides whether or not a word should be displayed, 
# based on the words appearances in a text. 
def helper(a, b, c, beg, end):
    beg = beg.split(".")
    end = end.split(".")
    a = list_of_lists(a)
    for i in range(len(a)):
        if len(beg) == 1 and len(end) == 1: # 1 subdivision
            if int(beg[0]) <= int(a[i][0]) <= int(end[0]):
                return c.append(b.title)
    
        elif len(beg) == 2 and len(end) == 2: # 2 subdivisions
            if a[i][0] != "" and int(beg[0]) <= int(a[i][0]):
                if int(end[0]) == int(beg[0]) and int(end[0]) >= int(a[i][0]):
                    if int(beg[1]) <= int(a[i][1]) and int(end[1]) >= int(a[i][1]):
                        return c.append(b.title)
                elif int(end[0]) > int(a[i][0]):
			return c.append(b.title)
		elif int(end[0]) == int(a[i][0]) and int(end[1]) >= int(a[i][1]):
                        return c.append(b.title)

        elif len(beg) == 3 and len(end) == 3: #3 subdivisions
            if a[i][0] != ""  and int(beg[0]) <= int(a[i][0]) and int(end[0]) >= int(a[i][0]):
                if int(beg[1]) <= int(a[i][1]):
                    if int(end[1]) == int(a[i][1]):
                        if int(beg[2]) <= int(a[i][2]) and int(end[2]) >= int(a[i][2]):
                            return c.append(b.title)
                    elif int(end[1]) > int(a[i][1]):
                            return c.append(b.title)

	elif len(beg) == 1 and len(end) == 2:
	    if a[i][0] != "" and int(a[i][0]) >= int(beg[0]) and int(end[0]) >= int(a[i][0]):
		if int(a[i][1]) <= int(end[1]):
			return c.append(b.title)

	elif len(beg) == 1 and len(end) == 3:
	    if a[i][0] != "" and int(a[i][0]) >= int(beg[0]) and int(end[0]) >= int(a[i][0]):
		if int(end[0]) > int(a[i][0]):
			return c.append(b.title)
		elif int(end[0]) == int(a[i][0]):
			if int(a[i][1]) < int(end[1]):
				return c.append(b.title)
			elif int(a[i][1]) == int(end[1]) and int(a[i][2]) <= int(end[2]):
				return c.append(b.title)

	elif len(beg) == 2 and len(end) == 1:
	   if a[i][0] != "" and int(a[i][0]) >= int(beg[0]) and int(end[0]) >= int(a[i][0]):
		if int(a[i][0]) > int(beg[0]):
			return c.append(b.title)
		elif int(a[i][0]) == int(beg[0]):
			if int(a[i][1]) >= int(beg[1]):
				return c.append(b.title)

	elif len(beg) == 2 and len(end) == 3:
	   if a[i][0] != "" and int(a[i][0]) >= int(beg[0]) and int(end[0]) >= int(a[i][0]):
		if int(a[i][0]) == int(beg[0]) and int(a[i][1]) >= int(beg[1]):
			if int(a[i][0]) == int(end[0]):
				if int(a[i][1]) == int(end[1]) and int(a[i][2]) <= int(end[2]):
					return c.append(b.title)
				elif int(a[i][1]) < int(end[1]):
					return c.append(b.title)	
			elif int(a[i][0]) < int(end[0]):
				return c.append(b.title)
		elif int(a[i][0]) > int(beg[0]):
			if int(a[i][0]) == int(end[0]):
                                if int(a[i][1]) == int(end[1]) and int(a[i][2]) <= int(end[2]):
                                        return c.append(b.title)
                                elif int(a[i][1]) < int(end[1]):
                                        return c.append(b.title)
                        elif int(a[i][0]) < int(end[0]):
                                return c.append(b.title)

	elif len(beg) == 3 and len(end) == 1:
           if a[i][0] != "" and int(a[i][0]) >= int(beg[0]) and int(end[0]) >= int(a[i][0]):
                if int(a[i][0]) == int(beg[0]):
                        if int(a[i][1]) == int(beg[1]) and int(a[i][2]) > int(beg[2]):
                                return c.append(b.title)
                        elif int(a[i][1]) > int(beg[1]):
                                return c.append(b.title)
                elif int(a[i][0]) > int(beg[0]):
                        return c.append(b.title)


	elif len(beg) == 3 and len(end) == 2:
	   if a[i][0] != "" and int(a[i][0]) >= int(beg[0]) and int(end[0]) >= int(a[i][0]):
		if int(a[i][0]) == int(end[0]) and int(a[i][1]) <= int(end[1]):
			if int(a[i][0]) == int(beg[0]):
				if int(a[i][1]) == int(beg[1]) and int(a[i][2]) >= int(beg[2]):
					return c.append(b.title)
				elif int(a[i][1]) > int(beg[1]):
					return c.append(b.title)
			elif int(a[i][0]) > int(beg[0]):
				return c.append(b.title)
		elif int(a[i][0]) < int(end[0]):
			if int(a[i][0]) == int(beg[0]):
                                if int(a[i][1]) == int(beg[1]) and int(a[i][2]) >= int(beg[2]):
                                        return c.append(b.title)
                                elif int(a[i][1]) > int(beg[1]):
                                        return c.append(b.title)
                        elif int(a[i][0]) > int(beg[0]):
                                return c.append(b.title)

	    
def core_helper(x, y, z, beg, end):
	if y is not None and y != "":
		if int(beg) <= int(y) and int(end) >= int(y):
			return z.append(x.title)

def greek_core_helper(x, y, z, beg, end):
	if y is not None and y != "" and y != "#N/A":
        	if int(beg) <= int(y) and int(end) >= int(y):
	               	return z.append(x.title)



def greek_helper(a, b, c, beg, end):
    beg = beg.split(".")
    end = end.split(".")
    a = list_of_lists(a)
    for i in range(len(a)):
        if len(beg) == 1 and len(end) == 1:
            if int(beg[0]) <= int(a[i][0]) <= int(end[0]):
                return c.append(b.title)

	elif len(beg) == 1 and len(end) == 2 and len(a[i]) == 1:
	    if int(beg[0]) <= int(a[i][0]) <= int(end[0]):
		return c.append(b.title)
	
	elif len(beg) == 1 and len(end) == 2 and len(a[i]) ==2:
	    if int(a[i][0]) >= int(beg[0]):
		if int(a[i][0]) == int(end[0]) and a[i][1] <= end[1]:
			return c.append(b.title)
		elif int(a[i][0]) < int(end[0]):
			return c.append(b.title)
	
	elif len(beg) == 2 and len(end) == 1 and len(a[i]) == 1:
	    if int(beg[0]) <= int(a[i][0]) <= int(end[0]):
		return c.append(b.title)

	elif len(beg) == 2 and len(end) == 1 and len(a[i]) == 2:
	    if int(end[0]) >= int(a[i][0]):
		if int(a[i][0]) == int(beg[0]) and a[i][1] >= beg[1]:
			return c.append(b.title)
		elif int(a[i][0]) > int(beg[0]):
			return c.append(b.title)

        elif len(beg) == 2 and len(end) ==2 and len(a[i]) == 2:
            if int(beg[0]) <= int(a[i][0]):
                if int(end[0]) == int(beg[0]) and int(end[0]) >= int(a[i][0]):
                    if beg[1] <= a[i][1] and end[1] >= a[i][1]:
                        return c.append(b.title)
                elif int(end[0]) > int(a[i][0]):
                        return c.append(b.title)
                elif int(end[0]) == int(a[i][0]) and end[1] >= a[i][1]:
                        return c.append(b.title)

	elif len(beg) == 2 and len(end) == 2 and len(a[i]) == 1:
	    if int(beg[0]) <= int(a[i][0]): 
		if int(a[i][0]) <= int(end[0]):
			return c.append(b.title) 
	

                        return c.append(b.title)
	