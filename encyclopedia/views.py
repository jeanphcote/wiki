import re
from django.forms import fields, widgets
from django.forms.widgets import HiddenInput, Widget
from django.shortcuts import redirect, render

from . import util
import encyclopedia

import markdown2
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import secrets


class TitleSeachForm(forms.Form):
    searched = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Search encyclopedia','autocomplete':'off'})) #attrs={'size': '20'}

class CreateEntryForm(forms.Form):
    entry_title = forms.CharField(label="Enter entry title", max_length=100, widget=forms.TextInput(attrs={'autocomplete':'off'}))
    entry_content = forms.CharField(label=False, widget=forms.Textarea(attrs={'placeholder': 'Enter entry content here', 'autocomplete':'off'}))

class EditEntryForm(forms.Form):
    entry_content = forms.CharField(label=False, widget=forms.Textarea(attrs={'placeholder': 'Enter entry content here', 'autocomplete':'off'}))


def index(request):
    if request.method == "POST":
        form = TitleSeachForm(request.POST)
        if form.is_valid():
            searched = form.cleaned_data["searched"]
            return redirect(f"title.html?title={searched}")
        else:
            return render(request, "index.html", {
                "form" : form
            })   
    else:
        form = TitleSeachForm()
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form":TitleSeachForm()
        })

def title(request, title):
    if request.method=='GET':
        title = request.GET.get('title')

    entries = util.list_entries()
    partial_match = [x for x in entries if str(title) in x] #casting to string to avoid error message
    if title in entries:
        raw_content = util.get_entry(title)
        content = markdown2.markdown(raw_content)
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "content" : content,
            "form":TitleSeachForm()
        })
    # Here I need to test if the title matches partially an entry
    elif partial_match:
        list_of_matches = partial_match
        return render(request, "encyclopedia/searching.html", {
            "matches": list_of_matches,
            "form":TitleSeachForm()
        })

    else:
        #return render(request, "encyclopedia/notfound.html", {
        return render(request, "encyclopedia/searching.html", {
             "title": title,
             "form":TitleSeachForm()
        })

def searching(request, title):
    if request.method=='GET':
        title = request.GET.get('title')
        entries = util.list_entries()
        if title in entries:
            raw_content = util.get_entry(title)
            content = markdown2.markdown(raw_content)
            return render(request, "encyclopedia/search.html", {
                "title": title,
                "content" : content
            })
        else:
            return render(request, "encyclopedia/search.html", {
                "title": title
            })

def create(request):
    if request.method=='POST':
        form = CreateEntryForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data['entry_title']
            entry_content = form.cleaned_data['entry_content']
            entries = util.list_entries()
            if entry_title in entries:
                return render(request, "encyclopedia/error.html", {
                    "entry": entry_title,
                    "form":TitleSeachForm()
                })
            else:
                save_entry = util.save_entry(entry_title, entry_content)
                raw_content = util.get_entry(entry_title)
                content = markdown2.markdown(raw_content)
                return render(request, "encyclopedia/title.html", {
                    "title": entry_title,
                    "content" : content
                })
    else:
        return render(request, "encyclopedia/create.html", {
            "form":TitleSeachForm(),
            "form2":CreateEntryForm()
                })

def edit(request):
    if request.method=='GET':
        entry_title = request.GET.get('entry_title')
        raw_content = util.get_entry(entry_title)
        entry_content = markdown2.markdown(raw_content)
        return render(request, "encyclopedia/edit.html", {
                "entry_title": entry_title,
                "form3": EditEntryForm(initial={'entry_content':raw_content}),
                "form":TitleSeachForm()
                }) 
    else:
        form = EditEntryForm(request.POST)
        if form.is_valid():
            entry_title = request.POST.get('entry_title')
            entry_content = form.cleaned_data['entry_content']
            save_entry = util.save_entry(entry_title, entry_content)
            raw_content = util.get_entry(entry_title)
            content = markdown2.markdown(raw_content)
            return render(request, "encyclopedia/title.html", {
                "title": entry_title,
                "content" : content
            })

def random(request):
    if request.method=='GET':
        entries = util.list_entries()
        if entries:
            selected_title = secrets.choice(entries)
            raw_content = util.get_entry(selected_title)
            content = markdown2.markdown(raw_content)
            return render(request, "encyclopedia/title.html", {
                "title": selected_title,
                "content" : content,
                "form":TitleSeachForm()
            })
    else:
        return render(request, "encyclopedia/index.html", {
             "form":TitleSeachForm()
        })

def wiki(request, string):
    if request.method=='GET':
        title = string
        entries = util.list_entries()
        if title in entries:
            raw_content = util.get_entry(title)
            content = markdown2.markdown(raw_content)
            return render(request, "encyclopedia/title.html", {
                "title": title,
                "content" : content,
                "form":TitleSeachForm() 
            })
        else:
            return render(request, "encyclopedia/searching.html", {
                "title": title,
                "form":TitleSeachForm()
            })