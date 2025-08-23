from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("projects/", views.projects, name="projects"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path("projects/<slug:slug>/partial/", views.project_detail_partial, name="project_detail_partial"),
    path("blog/", views.blog, name="blog"),
    path("blog/<slug:slug>/", views.post_detail, name="post_detail"),
    path("resume/", views.resume, name="resume"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("api/contact/", views.contact_api, name="contact_api"),
    path("search/", views.search, name="search"),
    path("search.json", views.search_json, name="search_json"),
]