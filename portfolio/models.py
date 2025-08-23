from django.db import models
from django.urls import reverse
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=72, unique=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    summary = models.TextField()
    content = models.TextField(blank=True)
    roles = models.CharField(max_length=200, blank=True)
    tools = models.CharField(max_length=200, blank=True)
    challenge = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    metrics = models.TextField(blank=True)
    hero_image_url = models.CharField(max_length=300, blank=True)
    featured = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)
    published = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-published"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"slug": self.slug})

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image_url = models.CharField(max_length=300)
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.project.title} image"

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    summary = models.TextField()
    content_markdown = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    published = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-published"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"slug": self.slug})

    @property
    def reading_time_minutes(self) -> int:
        words = len(self.content_markdown.split())
        return max(1, words // 200)

class Testimonial(models.Model):
    author_name = models.CharField(max_length=128)
    role = models.CharField(max_length=128, blank=True)
    content = models.TextField()
    featured = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.author_name} — {self.role}"

class Skill(models.Model):
    name = models.CharField(max_length=100)
    proficiency = models.PositiveIntegerField(default=80)
    category = models.CharField(max_length=100, default="General")

    def __str__(self):
        return f"{self.name} ({self.proficiency}%)"

class ContactSubmission(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.email} @ {self.created_at:%Y-%m-%d %H:%M}"