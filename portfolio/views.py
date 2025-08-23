from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, View

from .forms import ContactForm
from .models import Project, BlogPost, Tag, Testimonial, Skill, ContactSubmission

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["featured_projects"] = Project.objects.filter(featured=True)[:6]
        ctx["latest_posts"] = BlogPost.objects.all()[:6]
        ctx["testimonials"] = Testimonial.objects.filter(featured=True)[:5]
        ctx["skills"] = Skill.objects.all()[:12]
        return ctx

class ProjectListView(ListView):
    model = Project
    template_name = "projects/list.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        tag = self.request.GET.get("tag")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(summary__icontains=q) | Q(content__icontains=q))
        if tag:
            qs = qs.filter(tags__slug=tag)
        return qs.select_related().prefetch_related("tags")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tags"] = Tag.objects.all()
        ctx["active_tag"] = self.request.GET.get("tag", "")
        ctx["q"] = self.request.GET.get("q", "")
        return ctx

class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/detail.html"
    context_object_name = "project"

    def get_template_names(self):
        if self.request.GET.get("partial") == "1":
            return ["projects/partial_detail.html"]
        return [self.template_name]

class BlogListView(ListView):
    model = BlogPost
    template_name = "blog/list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        tag = self.request.GET.get("tag")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(summary__icontains=q) | Q(content_markdown__icontains=q))
        if tag:
            qs = qs.filter(tags__slug=tag)
        return qs.prefetch_related("tags")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tags"] = Tag.objects.all()
        ctx["active_tag"] = self.request.GET.get("tag", "")
        ctx["q"] = self.request.GET.get("q", "")
        return ctx

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = "blog/detail.html"
    context_object_name = "post"

class AboutView(TemplateView):
    template_name = "about.html"

class ResumeView(TemplateView):
    template_name = "resume.html"

class ContactView(View):
    def get(self, request):
        return render(request, "contact.html", {"form": ContactForm()})

    def post(self, request):
        form = ContactForm(request.POST)
        is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"
        if form.is_valid():
            ip = request.META.get("REMOTE_ADDR")
            ContactSubmission.objects.create(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                message=form.cleaned_data["message"],
                ip_address=ip,
            )
            send_mail(
                subject=f"Portfolio contact from {form.cleaned_data['name']}",
                message=form.cleaned_data["message"],
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[form.cleaned_data["email"]],
                fail_silently=True,
            )
            if is_ajax:
                return JsonResponse({"ok": True, "message": "Thanks! I’ll reply shortly."})
            messages.success(request, "Thanks! I’ll reply shortly.")
            return render(request, "contact.html", {"form": ContactForm()})
        if is_ajax:
            return JsonResponse({"ok": False, "errors": form.errors}, status=400)
        return render(request, "contact.html", {"form": form})

def search_page(request):
    q = request.GET.get("q", "")
    projects = Project.objects.filter(Q(title__icontains=q) | Q(summary__icontains=q))[:10]
    posts = BlogPost.objects.filter(Q(title__icontains=q) | Q(summary__icontains=q))[:10]
    return render(request, "home.html", {
        "featured_projects": projects,
        "latest_posts": posts,
        "testimonials": Testimonial.objects.filter(featured=True)[:5],
        "skills": Skill.objects.all()[:12],
        "search_query": q,
    })