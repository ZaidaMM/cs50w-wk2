from django import forms
import random
from django.urls import reverse
from django.shortcuts import redirect, render
from markdown2 import Markdown

from . import util

def md_to_html_converter(title):
    md_to_convert = util.get_entry(title)
    markdowner = Markdown()
    if md_to_convert == None:
        return None
    else:
        return markdowner.convert(md_to_convert)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = md_to_html_converter(title)
    if html_content == None:
        return render(request, 'encyclopedia/error.html', {
            'error_message': "The page requested was not found"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    if request.method == "POST":
        query = request.POST['q']
        entry = md_to_html_converter(query)
        if entry is not None:
            return render(request, 'encyclopedia/entry.html', {
                "title":query, 
                "content":entry
            })
        else:
            entries_list = util.list_entries()
            results = []
            for entry in entries_list:
                if query.lower() in entry.lower():
                    results.append(entry)
            return render(request, 'encyclopedia/search.html', {
                "results": results
            })

def add(request):
    if request.method == "GET":        
        return render(request, "encyclopedia/add.html")
    else: 
        title = request.POST['entry_title']
        content = request.POST['entry_content']
        duplicated_entry = md_to_html_converter(title)
        if duplicated_entry is not None:
            return render(request, 'encyclopedia/error.html', {
                "error_message": "Encyclopedia already exists."
            })
        else:
            util.save_entry(title, content)
            new_entry = md_to_html_converter(title)
            return render(request, 'encyclopedia/entry.html', {
                "title": title, "content": new_entry
            })

def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title) 
        return render(request, "encyclopedia/edit.html", {"title":title, "content": content})
    
def saved(request):
    if request.method == "POST": 
        title = request.POST['edit_title']
        content = request.POST['edit_content']
        util.save_entry(title, content)
        new_entry = md_to_html_converter(title)
        return render(request, 'encyclopedia/entry.html', {
            "title": title, "content": new_entry
        })
    
def random_choice(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    entry = md_to_html_converter(random_title)
    return render(request, "encyclopedia/entry.html", {
        "title":random_title, "content":entry
    })