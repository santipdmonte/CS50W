from django.shortcuts import render

from django.http import JsonResponse

from . import util

def index(request):
    entries = util.list_entries()

    if request.method == 'POST':
        title = request.POST.get('title')
        content = util.get_entry(title)

        # If true the title exists
        if content:
            cont_html = util.get_html(content)
            return render(request, "encyclopedia/entry.html",{
                "title": title,
                "cont_html": cont_html
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
    editing = False
    if request.method == 'POST':
        editing = True

        new_content = request.POST.get('new_content')
        save_edit = request.POST.get('save_edit')

        if save_edit:
            util.save_entry(title, new_content)
            editing = False

    content = util.get_entry(title)
    if content:
        cont_html = util.get_html(content)
        print(f"{cont_html=}")
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "cont_html": cont_html,
            "content": content,
            "editing": editing
        })
    
    print("NOT TITLE FOUND")
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        })

def newpage(request):
    if request.method == 'POST':

        title = request.POST.get('title')
        content = request.POST.get('content')

        # Validation
        cont_validation = util.get_entry(title)
        if cont_validation:
            error_message = "Exists a page with this title"
            return JsonResponse({'error': error_message})

        print(f"Saved. {title=} {content=}")
        util.save_entry(title, content)

        entries = util.list_entries()
        return render(request, "encyclopedia/index.html", {
            "entries": entries
        })

    return render(request, "encyclopedia/newpage.html")

