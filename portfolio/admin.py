from django.contrib import admin
from .models import Tag, Project, ProjectImage, BlogPost, Testimonial, Skill, ContactSubmission

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "featured", "published")
    list_filter = ("featured", "tags")
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "published")
    list_filter = ("tags",)
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("author_name", "role", "featured")
    list_filter = ("featured",)
    search_fields = ("author_name", "role")

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "proficiency")
    list_filter = ("category",)

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "ip_address")
    search_fields = ("name", "email", "message")