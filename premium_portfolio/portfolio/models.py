from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Project(TimeStampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    excerpt = models.TextField()
    content = models.TextField()
    roles = models.CharField(max_length=200, help_text="Comma-separated roles")
    tools = models.CharField(max_length=200, help_text="Comma-separated tools")
    image = models.CharField(max_length=300, help_text="Path or URL to hero image")
    featured = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name="projects", blank=True)
    published_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-published_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("project_detail", args=[self.slug])

    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.CharField(max_length=300, help_text="Path or URL")
    alt_text = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.project.title} image"

class BlogPost(TimeStampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    excerpt = models.TextField()
    content = models.TextField()
    image = models.CharField(max_length=300, help_text="Path or URL to hero image", blank=True)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    published_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-published_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.slug])

    @property
    def reading_time_minutes(self) -> int:
        words = len(self.content.split())
        return max(1, words // 200)

    def __str__(self):
        return self.title

class Testimonial(TimeStampedModel):
    quote = models.TextField()
    author = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f"{self.author} — {self.role}"

class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.PositiveIntegerField(default=80, help_text="0-100")
    category = models.CharField(max_length=100, default="General")

    def __str__(self):
        return f"{self.name} ({self.level}%)"

class ContactSubmission(TimeStampedModel):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.email} — {self.subject}"