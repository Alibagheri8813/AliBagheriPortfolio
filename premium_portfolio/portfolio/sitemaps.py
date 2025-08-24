from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project, BlogPost

class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

class BlogPostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return BlogPost.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ["home", "projects", "blog", "about", "resume", "contact"]

    def location(self, item):
        return reverse(item)

sitemaps = {
    "projects": ProjectSitemap,
    "posts": BlogPostSitemap,
    "static": StaticViewSitemap,
}