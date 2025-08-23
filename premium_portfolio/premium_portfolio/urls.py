from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from portfolio.sitemaps import sitemaps as portfolio_sitemaps
from portfolio.views import robots_txt

sitemaps_dict = portfolio_sitemaps

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("portfolio.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps_dict}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
]

handler404 = "django.views.defaults.page_not_found"