from django.urls import path
from . import views, api

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("projects/", views.ProjectListView.as_view(), name="projects"),
    path("projects/<slug:slug>/", views.ProjectDetailView.as_view(), name="project_detail"),
    path("blog/", views.BlogListView.as_view(), name="blog"),
    path("blog/<slug:slug>/", views.BlogDetailView.as_view(), name="blog_detail"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("resume/", views.ResumeView.as_view(), name="resume"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("search/", views.search_page, name="search"),
    path("api/search/", api.search_api, name="search_api"),
    path("privacy/", views.TemplateView.as_view(template_name="legal/privacy.html"), name="privacy"),
    path("terms/", views.TemplateView.as_view(template_name="legal/terms.html"), name="terms"),
]