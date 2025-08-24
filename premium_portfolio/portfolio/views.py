import json
import time
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from .models import Project, BlogPost, Testimonial, Skill, Tag, ContactSubmission
from .forms import ContactForm


def home(request):
    featured_projects = Project.objects.filter(featured=True)[:6]
    latest_posts = BlogPost.objects.all()[:6]
    testimonials = Testimonial.objects.all()[:5]
    skills = Skill.objects.all()
    return render(request, "home.html", {
        "featured_projects": featured_projects,
        "latest_posts": latest_posts,
        "testimonials": testimonials,
        "skills": skills,
    })


def projects(request):
    tag_slug = request.GET.get("tag")
    projects_qs = Project.objects.all()
    if tag_slug:
        projects_qs = projects_qs.filter(tags__slug=tag_slug)
    tags = Tag.objects.all()
    return render(request, "projects/index.html", {"projects": projects_qs, "tags": tags, "active_tag": tag_slug})


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, "projects/detail.html", {"project": project})


def project_detail_partial(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, "projects/partial.html", {"project": project})


def blog(request):
    tag_slug = request.GET.get("tag")
    posts = BlogPost.objects.all()
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    tags = Tag.objects.all()
    return render(request, "blog/index.html", {"posts": posts, "tags": tags, "active_tag": tag_slug})


def post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, "blog/detail.html", {"post": post})


def resume(request):
    return render(request, "resume.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    form = ContactForm()
    return render(request, "contact.html", {"form": form})


def _ip(request):
    # Simple IP retrieval; adjust if behind proxies/load balancers
    return request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip() or request.META.get("REMOTE_ADDR", "")


def contact_api(request):
    if request.method != "POST":
        return JsonResponse({"ok": False, "error": "Invalid method"}, status=405)

    form = ContactForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"ok": False, "error": "Invalid form", "details": form.errors}, status=400)

    ip = _ip(request)
    # Rate limit: 1 message per 60 seconds per IP
    cooldown_seconds = 60
    recent = ContactSubmission.objects.filter(ip_address=ip, created_at__gte=timezone.now() - timezone.timedelta(seconds=cooldown_seconds)).first()
    if recent:
        return JsonResponse({"ok": False, "error": "Too many requests, please wait a minute."}, status=429)

    # Recaptcha stub: if enabled, verify; else, pass
    if settings.RECAPTCHA_ENABLED:
        token = form.cleaned_data.get("recaptcha_token", "")
        if not token:
            return JsonResponse({"ok": False, "error": "Missing reCAPTCHA"}, status=400)
        # TODO: implement requests.post to Google's siteverify; keeping stubbed for this template
        time.sleep(0.05)  # simulate
        # assume ok if provided

    data = form.cleaned_data
    ContactSubmission.objects.create(
        name=data["name"],
        email=data["email"],
        subject=data["subject"],
        message=data["message"],
        ip_address=ip,
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
    )

    # Send email (console backend in dev)
    subject = f"Portfolio Contact: {data['subject']}"
    body = f"From: {data['name']} <{data['email']}>\n\n{data['message']}"
    to_email = getattr(settings, "CONTACT_RECIPIENT_EMAIL", settings.DEFAULT_FROM_EMAIL)
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [to_email], fail_silently=True)

    return JsonResponse({"ok": True})


def search(request):
    q = request.GET.get("q", "").strip()
    project_results = []
    post_results = []
    if q:
        project_results = Project.objects.filter(Q(title__icontains=q) | Q(excerpt__icontains=q) | Q(content__icontains=q))[:20]
        post_results = BlogPost.objects.filter(Q(title__icontains=q) | Q(excerpt__icontains=q) | Q(content__icontains=q))[:20]
    return render(request, "search.html", {"q": q, "project_results": project_results, "post_results": post_results})


def search_json(request):
    q = request.GET.get("q", "").strip()
    projects = []
    posts = []
    if q:
        projects = list(Project.objects.filter(Q(title__icontains=q) | Q(excerpt__icontains=q)).values("title", "slug")[:10])
        posts = list(BlogPost.objects.filter(Q(title__icontains=q) | Q(excerpt__icontains=q)).values("title", "slug")[:10])
    return JsonResponse({"projects": projects, "posts": posts})


def robots_txt(request):
    content = """User-agent: *\nAllow: /\nSitemap: {}/sitemap.xml\n""".format(request.build_absolute_uri("/").rstrip("/"))
    return HttpResponse(content, content_type="text/plain")