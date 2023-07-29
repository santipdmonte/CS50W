from django.shortcuts import render

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    description = util.get_entry(title)
    desc_html = util.get_html(description)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "description": desc_html
    })
