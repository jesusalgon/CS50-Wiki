from django.shortcuts import render, redirect
from markdown2 import markdown
from random import randint
from . import util
from . import forms


def index(request):
    if request.method == 'POST':
        search = request.POST.get('q')
        all_entries = util.list_entries()
        title_in_page = f"Results for <i>{search}</i>:"

        entries = list(filter(lambda x: search.lower() in x.lower(), all_entries))
        if not entries:
            title_in_page = f"No results found for <i>{search}.</i>"

        return render(request, "encyclopedia/search.html", {
            "entries": entries,
            "title_in_page": title_in_page
        })

    if request.method == 'GET':
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def entry(request, title):
    raw_content = util.get_entry(title)
    if raw_content:
        content = markdown(raw_content)

        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })

    return render(request, status=404, template_name="encyclopedia/not_found.html", context={
        "title": title
    })


def add_new_entry(request):
    url = '/new-page/'

    if request.method == 'POST':
        form = forms.NewEntryForm(request.POST)
        form_content = form.cleaned_data['content']
        if form.is_valid():
            form_title = form.cleaned_data['title'].capitalize()
            if f'# {form_title}\n' not in form_content:
                form_content = f'# {form_title}\n' \
                               f'{form_content}'
            util.save_entry(form_title, form_content)
            response = redirect(f'/wiki/{form_title}')

            return response
        else:
            return render(request, 'encyclopedia/new_entry.html', {
                'url': url,
                "form": forms.NewEntryForm(request.POST)
            })

    return render(request, 'encyclopedia/new_entry.html', {
        'url': url,
        "form": forms.NewEntryForm()
    })


def edit_page(request, title):
    url = f'/wiki/{title}/edit-page/'

    if request.method == 'POST':
        form = forms.EditEntryForm(request.POST)
        if form.is_valid():
            form_content = form.cleaned_data['content']
            if f'# {title}' not in form_content:
                form_content = f'# {title}\n' \
                               f'{form_content}'
            util.save_entry(title, form_content)
            response = redirect(f'/wiki/{title}')

            return response
        else:
            return render(request, 'encyclopedia/edit_entry.html', {
                'url': url,
                'form': forms.EditEntryForm(request.POST)
            })

    content = util.get_entry(title)
    if content:
        return render(request, 'encyclopedia/edit_entry.html', {
            'url': url,
            'title': title,
            'form': forms.EditEntryForm(initial={'content': content})
        })
    else:
        return render(request, status=404, template_name="encyclopedia/not_found.html", context={
            "title": title
        })


def go_to_random_page(request):
    titles = util.list_entries()
    n_titles = len(titles)
    random_title_pos = randint(0, n_titles - 1)
    random_title = titles[random_title_pos]

    return redirect(f'/wiki/{random_title}')

