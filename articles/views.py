import itertools
import json
from _ast import operator

from bson import json_util
from django.shortcuts import render
from .models import *
from pymongo import MongoClient
import json
from django.shortcuts import render, redirect
from .models import article
from .forms import ArticleSearch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pymongo import MongoClient
import re
from pprint import pprint
from django.shortcuts import get_object_or_404

cluster = MongoClient("mongodb+srv://dbuserdolphin:dbpassworddolphin@cluster0.h6bhx.mongodb.net/dolphin?retryWrites=true&w=majority")
db = cluster["dolphin"]
collection = db["articles_article"]
sys_collection = db["ontologies_ontology"]

cluster2 = MongoClient("mongodb+srv://new_user_587:nXxoVnTlNcva3Mro@cluster0.hngug.mongodb.net/<dbname>?retryWrites=true&w=majority")
db2 = cluster2["annotations"]
collection2 = db2["annotations"]



import datetime
from datetime import datetime
import pycountry


def all_articles(request):

    context = {}
    for i in range(50):
        context["articles_"+str(i)] = request.session.get("articles_"+str(i))

        dimensional_articles = context["articles_" + str(i)]
        paginated_articles = Paginator(dimensional_articles, 10)
        page_number = request.GET.get('page', None)
        article_page_ob = paginated_articles.get_page(page_number)

        for item in paginated_articles.object_list:
            authors = item['authors']
            keywords = item['keywords']
            b = json.loads(authors)
            c = json.loads(keywords)
            item['authors'] = b
            item['keywords'] = c

        context["article_page_ob_" + str(i)] = article_page_ob
        dimensional_articles.clear()

    return render(request, "all_articles.html", context)

def reqs(request):

    queries_0 = []
    queries_1 = []
    queries_2 = []


    if 'q_0' in request.GET:
        query = request.GET["q_0"]
        queriess = query.split(" ")
        queries_0 = queries_0 + queriess

    if 'q_1' in request.GET:
        query = request.GET["q_1"]
        queriess = query.split(" ")
        queries_1 = queries_1 + queriess

    if 'q_2' in request.GET:
        query = request.GET["q_2"]
        queriess = query.split(" ")
        queries_2 = queries_2 + queriess

    return queries_0, queries_1, queries_2

def synonymous(query):

    synonymous_words = []

    for q in query:
        synonymous = sys_collection.find({"label": {"$regex": r'\b' + q + r'\b', "$options": 'i'}})
        for s in synonymous:
            for i in s["synonymous"]:
                synonymous_words.append(i)

    return synonymous_words

def dimensional_search(request):

    context = {}
    index = 0
    my_array = []

    if request.GET:

        queries_0, queries_1, queries_2 = reqs(request)

        queries_0_sys = synonymous(queries_0)
        queries_1_sys = synonymous(queries_1)
        queries_2_sys = synonymous(queries_2)

        print(queries_0_sys)
        print(queries_0)

        context["queries_0"] = queries_0
        context["queries_1"] = queries_1
        context["queries_2"] = queries_2


        if len(queries_0_sys) >= 1:

            for a in queries_0_sys:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [a]
                index += 1
                my_array.clear()

        if len(queries_1_sys) >= 1:

            for b in queries_1_sys:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [b]
                index += 1
                my_array.clear()

        if len(queries_2_sys) >= 1:

            for c in queries_2_sys:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + c + r'\b' + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [c]
                index += 1
                my_array.clear()

        for (a, b, c) in itertools.zip_longest(queries_0, queries_1, queries_2):

            if a is None and b is not None:
                a = b
            if a is None and c is not None:
                a = c
            if b is None and a is not None:
                b = a
            if c is None and a is not None:
                c = a


            articles = collection.find({
                "$or": [
                    {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                              {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                              {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                            ]},

                    {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                              {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                              {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                            ]}
                ]
            })

            if a != b and a != c:
                context["q_" + str(index)] = [a, b, c]
                request.session["q_" + str(index)] = [a, b, c]

            if a == b and a == c:
                context["q_" + str(index)] = [a]
                request.session["q_" + str(index)] = [a]

            if a == c and a != b:
                context["q_" + str(index)] = [a, b]
                request.session["q_" + str(index)] = [a, b]

            for item in articles:
                my_array.append(item)

            context["articles_" + str(index)] = my_array
            request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

            context["total_count_" + str(index)] = len(my_array)
            index += 1
            my_array.clear()

        if len(queries_1) > 1:

            queries_1.reverse()

            for (a, b, c) in itertools.zip_longest(queries_0, queries_1, queries_2):

                if a is None and b is not None:
                    a = b
                if a is None and c is not None:
                    a = c
                if b is None and a is not None:
                    b = a
                if c is None and a is not None:
                    c = a

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                              ]},

                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                 ]}
                    ]
                })

                if a != b and a != c:
                    context["q_" + str(index)] = [a, b, c]
                    request.session["q_" + str(index)] = [a, b, c]

                if a == b and a == c:
                    context["q_" + str(index)] = [a]
                    request.session["q_" + str(index)] = [a]

                if a == c and a != b:
                    context["q_" + str(index)] = [a, b]
                    request.session["q_" + str(index)] = [a, b]

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                index += 1
                my_array.clear()

        if len(queries_2) > 1:

            queries_2.reverse()

            for (a, b, c) in itertools.zip_longest(queries_0, queries_1, queries_2):

                if a is None and b is not None:
                    a = b
                if a is None and c is not None:
                    a = c
                if b is None and a is not None:
                    b = a
                if c is None and a is not None:
                    c = a

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                ]},

                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                               ]}
                    ]
                })

                if a != b and a != c:
                    context["q_" + str(index)] = [a, b, c]
                    request.session["q_" + str(index)] = [a, b, c]

                if a == b and a == c:
                    context["q_" + str(index)] = [a]
                    request.session["q_" + str(index)] = [a]

                if a == c and a != b:
                    context["q_" + str(index)] = [a, b]
                    request.session["q_" + str(index)] = [a, b]

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                index += 1
                my_array.clear()

        if len(queries_1) > 1:

            queries_1.reverse()

            for (a, b, c) in itertools.zip_longest(queries_0, queries_1, queries_2):

                if a is None and b is not None:
                    a = b
                if a is None and c is not None:
                    a = c
                if b is None and a is not None:
                    b = a
                if c is None and a is not None:
                    c = a

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                              ]},

                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                ]}
                    ]
                })

                if a != b and a != c:
                    context["q_" + str(index)] = [a, b, c]
                    request.session["q_" + str(index)] = [a, b, c]

                if a == b and a == c:
                    context["q_" + str(index)] = [a]
                    request.session["q_" + str(index)] = [a]

                if a == c and a != b:
                    context["q_" + str(index)] = [a, b]
                    request.session["q_" + str(index)] = [a, b]

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                index += 1
                my_array.clear()

        for (a, b, c) in itertools.zip_longest(queries_0, queries_1, queries_2):

            if a is not None:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [a]
                index += 1
                my_array.clear()

            if b is not None:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [b]
                index += 1
                my_array.clear()

            if c is not None:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [c]
                index += 1
                my_array.clear()

            if a is not None and b is not None:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [a, b]
                index += 1
                my_array.clear()

            if a is not None and c is not None:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [a, c]
                index += 1
                my_array.clear()

            if b is not None and c is not None:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [b, c]
                index += 1
                my_array.clear()

        queries_1.reverse()
        queries_2.reverse()

        for (a, b, c) in itertools.zip_longest(queries_0, queries_1, queries_2):

            if a is not None and b is not None:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [a, b]
                index += 1
                my_array.clear()

            if a is not None and c is not None:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [a, c]
                index += 1
                my_array.clear()

            if b is not None and c is not None:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [b, c]
                index += 1
                my_array.clear()

        queries_1.reverse()

        for (b, c) in itertools.zip_longest(queries_1, queries_2):

            if b is not None and c is not None:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [b, c]
                index += 1
                my_array.clear()


    return render(request, "dimension.html", {'context': context})


def parse_json(data):
    return json.loads(json_util.dumps(data))


def query_process(query):

    new_query = []
    stopwords = ['and', 'or', 'but', 'And', 'But', 'Or']
    for q in query:
        q = ' '.join(filter(lambda x: x not in stopwords, q.split()))
        new_query.append(q)
    return new_query

# Function for splitting query terms with commas

def split_line(query):
    result = [word.strip() for word in query.split(',')]
    return result

# Basic search function
def home(request):

#Transferred variables with request; query, start_date, end_date, country

    all_articles = article.objects.all()
    form = ArticleSearch()
    total_articles = all_articles.count()
    context = {
        "total_articles": total_articles,
        "form": form,
    }
    query = request.GET.get('abstract')
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    country = request.GET.get('country')
    global invalid_chars
    invalid_chars = {',', '\\', ']', "'", '=', '<', '+', '_', '`', ')', '@', '|', '/', '&', '#', '%', '}', '{', '-', '>', '*', ':', '?', '[', ';', '~', '!', '$', '.', '(', '^', '"'}


    if request.method == 'POST':

        pattern = r'(?i)\b' + query + r'\b'
        regex = re.compile(pattern)
        articles = []
        articl = collection.find({"$or": [{"abstract": {"$regex": regex}}, {"title": {"$regex": regex}}]})
        for item in articl:
            articles.append(item)

        searched_total_articles = articl.count()
        paginated_articles = Paginator(articles, 10)
        page_number = request.GET.get('page', None)
        article_page_ob = paginated_articles.get_page(page_number)
        context = {
            "total_articles": total_articles,
            "searched_articles": searched_total_articles,
            "articles": articles,
            "form": form,
            "article_page_ob": article_page_ob,
            "query": query
        }

# Recevived request method and processed thru from here

    elif request.method == 'GET':

# Query string is processed

        if query:
            queris = split_line(query)
            queris = list(filter(None, queris))
            dt_start = start_date.replace("-", ", ")
            dt_start= dt_start.replace(" 0", " ")
            dt_end = end_date.replace("-", ", ")
            dt_end = dt_end.replace(" 0", " ")
            start_year, start_month, start_day = dt_start.split(", ",2)
            end_year, end_month, end_day = dt_end.split(", ",2)
            articles = []
            counter = 0
            my_list=[]
            queris=query_process(queris)

# Regex is applied to process query term

            for que in queris:
                quer = ""
                pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                quer2 = re.findall(pat, que)
                syn_reg= r'(?i)\b' + que + r'\b'

                syn_regex = re.compile(syn_reg)
                counter+= 1
                que = re.findall(pat, que)
                pp = r''
                for qu in que:
                    if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                        po= r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                        tmp=  pp + po
                        pp=tmp
                    else:
                        pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                        tmp= pp + pt
                        pp= tmp
                regex = re.compile(pp)

# Articles are collected based on the search term

                articl = collection.find({"$and":
                                              [{"$or":
                                                    [{"abstract": {"$regex": regex}}, {"title": {"$regex": regex}}]},
                                               {"publication_date": {"$gte": datetime(int(start_year), int(start_month), int(start_day), 1, 30), "$lte": datetime(int(end_year), int(end_month), int(end_day), 1, 30)}},
                                               {"authors": {"$regex": country}}
                                               ]
                                          })
                sys_words = []

# Synonmous words are found

                synonymous = sys_collection.find({"label": {"$regex": syn_regex }})
                for s in synonymous:
                    for i in s["synonymous"]:
                        sys_words.append(i)
                my_list = my_list+sys_words
                tmp_syn = []
                for syn in sys_words:
                    if any(char in invalid_chars for char in syn):
                        continue
                    else:
                        syn = r'(?i)\b' + syn + r'\b'
                        syn = re.compile(syn)

# Articles are collected based on the synonymous words

                        articl2 = collection.find({"$and":
                                                    [{"$or": [{"abstract": {"$regex": syn}}, {"title": {"$regex": syn}}]},
                                                        {"publication_date": {"$gte": datetime(int(start_year), int(start_month), int(start_day), 1, 30), "$lte": datetime(int(end_year), int(end_month), int(end_day), 1, 30)}},
                                                        {"authors": {"$regex": country}}
                                                        ]
                                                })
                        for i in articl2:
                            tmp_syn.append(i)



# Final collection of articles are formed here. Check is made to avoid duplicate articles for both query term
# and its synonyms and child classes.

                if len(articles) == 0 and counter == 1:
                    #tmp_arc=[]
                    for item in articl:
                        articles.append(item)
                    for it in tmp_syn:
                        if it in articles:
                            continue
                        else:
                            articles.append(it)

                else:
                    temp_arc=[]
                    for a in articl:
                        if a in articles:
                            temp_arc.append(a)
                    for ite in tmp_syn:
                        if ite in articles and ite not in temp_arc:
                            temp_arc.append(ite)

                    articles = temp_arc




            searched_total_articles = len(articles)

# Pagination of the pages are handled here.

            paginated_articles = Paginator(articles, 10)
            page_number = request.GET.get('page', None)
            country_new = request.GET.get('country', None)
            article_page_ob = paginated_articles.get_page(page_number)
            for item in paginated_articles.object_list:
                authors = item['authors']
                keywords = item['keywords']
                b = json.loads(authors)
                c = json.loads(keywords)
                item['authors'] = b
                item['keywords'] = c
            context = {
                "total_articles": total_articles,
                "searched_articles": searched_total_articles,
                "articles": articles,
                "form": form,
                "article_page_ob": article_page_ob,
                "query": query,
                "queris": queris,
                "my_list": my_list,
                "start_date": start_date,
                "end_date": end_date,
                "country": country_new,

            }


    return render(request, "articles.html", context)

# Article detail page is defined here

def article_detail(request, pubmed_id):

# Required parameters are defined and assigned

    all_articles = article.objects.all()
    form = ArticleSearch(request.POST or None)
    total_articles = all_articles.count()
    detail_article = article.objects.get(pubmed_id = pubmed_id)
    idd = detail_article.id
    tit = detail_article.title
    abst = detail_article.abstract
    keyw = detail_article.keywords
    jour = detail_article.journal
    pub_date = detail_article.publication_date.date()
    auth = detail_article.authors
    conc= detail_article.conclusions
    res= detail_article.results
    copy = detail_article.copyrights
    dooi = detail_article.doi

    context = {
         "form": form,
         "idd" : idd,
         "tit" : tit,
         "abst" : abst,
         "keyw" : keyw,
         "jour" : jour,
         "pub_date" : pub_date,
         "auth" : auth,
         "conc" : conc,
         "res" : res,
         "copy" : copy,
         "dooi" : dooi,
         "pubmed_id" : pubmed_id
    }
    query = request.GET.get('abstract', '')
    if request.method == 'POST':

        pattern = r'(?i)\b' + query + r'\b'
        regex = re.compile(pattern)
        articles = []
        articl = collection.find({"$or": [{"abstract": {"$regex": regex}}, {"title": {"$regex": regex}}]})
        for item in articl:
            articles.append(item)

        searched_total_articles = articl.count()
        paginated_articles = Paginator(articles, 10)
        page_number = request.GET.get('page', None)
        article_page_ob = paginated_articles.get_page(page_number)
        context = {
            "total_articles": total_articles,
            "searched_articles": searched_total_articles,
            "articles": articles,
            "form": form,
            "article_page_ob": article_page_ob,
            "query": query
        }

# Get request is handled here.

    elif request.method == 'GET':

# Regex is applied to query term to process query term

        if query:
            pattern = r'(?i)\b' + query + r'\b'
            regex = re.compile(pattern)
            articles = []

# Articles are collected based on request

            articl = collection.find({"$or": [{"abstract": {"$regex": regex}}, {"title": {"$regex": regex}}]})
            for item in articl:
                articles.append(item)

            searched_total_articles = articl.count()

# Pagination is applied just in case

            paginated_articles = Paginator(articles, 10)
            page_number = request.GET.get('page', None)
            article_page_ob = paginated_articles.get_page(page_number)

            context = {
                "total_articles": total_articles,
                "searched_articles": searched_total_articles,
                "articles": articles,
                "form": form,
                "article_page_ob": article_page_ob,
                "query": query
            }

    return render(request, "articles_detail.html", context)