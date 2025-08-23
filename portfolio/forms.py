from django import forms
from django.conf import settings
import requests

class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={"placeholder": "Your name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "you@example.com"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "placeholder": "How can I help?"}))
    recaptcha_token = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned = super().clean()
        token = cleaned.get("recaptcha_token")
        site_key = settings.RECAPTCHA_SITE_KEY
        secret_key = settings.RECAPTCHA_SECRET_KEY
        # If keys missing, skip verification (stubbed)
        if site_key and secret_key:
            try:
                resp = requests.post(
                    "https://www.google.com/recaptcha/api/siteverify",
                    data={"secret": secret_key, "response": token},
                    timeout=5,
                )
                ok = resp.json().get("success")
                if not ok:
                    raise forms.ValidationError("reCAPTCHA validation failed.")
            except Exception:
                raise forms.ValidationError("reCAPTCHA verification error, try again.")
        return cleaned