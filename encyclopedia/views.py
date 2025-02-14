from django.shortcuts import render, redirect

from . import util
from django.http import HttpResponse
import markdown2

def index(request):
    list_entries = ["CSS", "Django", "Git", "HTML", "Python"]
    return render(request, "encyclopedia/index.html", {
        "list_entries": list_entries
    })

def entries(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    content_html = markdown2.markdown(util.get_entry(title))
    return render(request, "encyclopedia/entries.html", {
        "title": title,
        "content": content_html
    })

def search(request):
    query = request.GET.get('q', '')

    if util.get_entry(query):
        return redirect('entries', title=query)
    else: # error here ?
        list_entries = util.list_entries()
        results = [entry for entry in list_entries if query.lower() in entry.lower()]

        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "results": results
        })