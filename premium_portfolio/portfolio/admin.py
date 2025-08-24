from django.contrib import admin
from .models import Tag, Project, ProjectImage, BlogPost, Testimonial, Skill, ContactSubmission

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "featured", "published_at")
    list_filter = ("featured", "tags")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at")
    list_filter = ("tags",)
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("author", "role")

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "level")

admin.site.register(Tag)
admin.site.register(ContactSubmission)