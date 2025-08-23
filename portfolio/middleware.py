from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.conf import settings
from .models import ContactSubmission

class RateLimitMiddleware:
    """
    Simple contact form rate limiter:
    - Limits one submission per 60s per IP
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.endswith("/contact/") and request.method == "POST":
            ip = request.META.get("REMOTE_ADDR")
            if ip:
                recent = ContactSubmission.objects.filter(
                    ip_address=ip, created_at__gte=timezone.now() - timedelta(seconds=60)
                ).exists()
                if recent:
                    if request.headers.get("x-requested-with") == "XMLHttpRequest":
                        return JsonResponse({"ok": False, "message": "Too many requests. Please wait."}, status=429)
                    from django.contrib import messages
                    messages.error(request, "Too many requests. Please wait a minute.")
        return self.get_response(request)

class ContentSecurityPolicyMiddleware:
    """
    Example CSP header (relaxed). Enable via CSP_ENABLED=1.
    Adjust sources before production hardening.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if getattr(settings, "CSP_ENABLED", False):
            csp = (
                "default-src 'self'; "
                "img-src 'self' data: https:; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                "font-src 'self' https://fonts.gstatic.com; "
                "script-src 'self'; "
                "connect-src 'self'; "
                "base-uri 'self'; frame-ancestors 'none'"
            )
            response.headers["Content-Security-Policy"] = csp
        return response