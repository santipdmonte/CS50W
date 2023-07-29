from django.shortcuts import render

from . import util

def index(request):
    entries = util.list_entries()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = util.get_entry(title)

        # If true the title exists
        if description:
            desc_html = util.get_html(description)
            return render(request, "encyclopedia/entry.html",{
                "title": title,
                "description": desc_html
            })
        
        # Find similar titles
        entries = [entry for entry in entries if title.lower() in entry.lower()] 
        return render(request, "encyclopedia/index.html", {
            "entries": entries
        })
        
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def entry(request, title):
    description = util.get_entry(title)
    if description:
        desc_html = util.get_html(description)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "description": desc_html
        })
    
    print("NOT TITLE FOUND")
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
        })

def newpage(request):
    if request.method == 'POST':

        title = request.POST.get('title')
        content = request.POST.get('content')

        # Validations ################################################

        print(f"Saved. {title=} {content=}")
        util.save_entry(title, content)

        entries = util.list_entries()
        return render(request, "encyclopedia/index.html", {
            "entries": entries
        })

    return render(request, "encyclopedia/newpage.html")

