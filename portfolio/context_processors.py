from django.conf import settings

def settings_context(_request):
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_DOMAIN": settings.SITE_DOMAIN,
        "GA_MEASUREMENT_ID": settings.GA_MEASUREMENT_ID,
        "RECAPTCHA_SITE_KEY": settings.RECAPTCHA_SITE_KEY,
    }