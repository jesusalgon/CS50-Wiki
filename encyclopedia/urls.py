from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("new-page", views.add_new_entry, name="create_new_page"),
    path("wiki/<str:title>/edit-page/", views.edit_page, name="edit_page"),
    path("random-page/", views.go_to_random_page, name="random_page")
]
