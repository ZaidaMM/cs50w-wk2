from django.shortcuts import render
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