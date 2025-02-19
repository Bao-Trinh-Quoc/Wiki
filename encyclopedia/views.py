from django.shortcuts import render, redirect

from . import util
from django.http import HttpResponse
import markdown2
import random

def index(request):
    list_entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "list_entries": list_entries
    })

def entries(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    # convert markdown to html
    content_html = markdown2.markdown(util.get_entry(title))

    return render(request, "encyclopedia/entries.html", {
        "title": title,
        "content": content_html
    })

def search(request):
    query = request.GET.get('q', '')

    # If the query is an exact match of an entry title
    if util.get_entry(query):
        return redirect('entries', title=query)
    else: # if the query is a substring of an entry title
        list_entries = util.list_entries()
        results = [entry for entry in list_entries if query.lower() in entry.lower()]
        # return the relevant entries
        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "results": results
        })
    
def create(request):
    # when user click create button
    if request.method == "POST":
        # get title and content from the form data
        title = request.POST.get("title")
        content = request.POST.get("content")
        # if entry already exists
        if util.get_entry(title):
            return render(request, "encyclopedia/create.html", {
                "error": "Entry already exists"
            })
        
        util.save_entry(title, content)
        return redirect('entries', title=title)
    
    return render(request, "encyclopedia/create.html")

def edit(request, title):
    # when user click save button
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect('entries', title=title)
    
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def random_entry(request):
    list_entries = util.list_entries()
    title = random.choice(list_entries)
    return redirect('entries', title=title)