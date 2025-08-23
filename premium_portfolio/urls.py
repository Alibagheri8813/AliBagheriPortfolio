from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from portfolio.sitemaps import sitemaps_map

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("portfolio.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps_map}, name="django.contrib.sitemaps.views.sitemap"),
    re_path(r"^robots\.txt$", TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain"
    ), name="robots"),
]