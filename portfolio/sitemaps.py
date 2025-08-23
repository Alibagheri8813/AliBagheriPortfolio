from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project, BlogPost

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ["home", "projects", "blog", "about", "resume", "contact", "privacy", "terms"]

    def location(self, item):
        return reverse(item)

class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Project.objects.all()

class BlogPostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return BlogPost.objects.all()

sitemaps_map = {
    "static": StaticViewSitemap,
    "projects": ProjectSitemap,
    "blog": BlogPostSitemap,
}