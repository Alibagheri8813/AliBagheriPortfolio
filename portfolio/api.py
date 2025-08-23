from django.http import JsonResponse
from django.db.models import Q
from .models import Project, BlogPost

def search_api(request):
    q = request.GET.get("q", "")
    projects = list(
        Project.objects.filter(Q(title__icontains=q) | Q(summary__icontains=q))
        .values("title", "slug")[:10]
    )
    posts = list(
        BlogPost.objects.filter(Q(title__icontains=q) | Q(summary__icontains=q))
        .values("title", "slug")[:10]
    )
    return JsonResponse({"projects": projects, "posts": posts})