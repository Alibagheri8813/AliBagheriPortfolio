from django.conf import settings

def site_settings(request):
    canonical = request.build_absolute_uri() if request and request.path else ""
    return {
        "SITE_NAME": "Premium Portfolio",
        "GA_MEASUREMENT_ID": getattr(settings, "GA_MEASUREMENT_ID", ""),
        "RECAPTCHA_SITE_KEY": getattr(settings, "RECAPTCHA_SITE_KEY", ""),
        "CANONICAL_URL": canonical,
    }