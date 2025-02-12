from django.shortcuts import render

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