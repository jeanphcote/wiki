from django.urls import path, re_path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.title, name="title"),
    path("<str:title>", views.searching, name="searching"),
    path("create/", views.create, name="create"),
    path("edit/", views.edit, name="edit"),
    path("random/", views.random, name="random"),
    path("wiki/<str:string>", views.wiki, name="wiki"),

]
