# Premium Portfolio (Django 4.x)

An ultra‑premium, modern portfolio for a high‑performing creator (developer/designer/student). Mobile‑first, accessible, SEO/performance‑optimized, with projects, case studies, blog, resume, testimonials, contact, sitemap/robots, tests, CI, and deploy files.

## Features
- Projects grid with tags/filters, deep‑linkable case study modal, lightbox gallery
- Blog with tags, reading time, structured data, OpenGraph/Twitter
- Resume page + downloadable PDF placeholder
- Contact form (AJAX) with CSRF + simple rate limiting (per IP cooldown)
- Client-side instant search + server search fallback
- Sitemap.xml + robots.txt (dynamic)
- Dark mode toggle (persists), animations with prefers‑reduced‑motion support
- Consent banner gating GA until accepted
- Security headers (CSP example), CSRF protection, safe templates
- Tests (views, APIs, sitemap) and GitHub Actions CI
- Dockerfile + Procfile, Whitenoise static serving

## Quickstart
```bash
# 1) Setup
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env

# 2) Configure (edit .env)
# - DJANGO_SECRET_KEY: set a strong secret
# - ALLOWED_HOSTS: e.g. localhost,127.0.0.1
# - GA_MEASUREMENT_ID (optional)
# - RECAPTCHA_* (optional dev stub included)

# 3) DB + demo data
python manage.py migrate
python manage.py seed_demo

# 4) Run
python manage.py runserver
```

Open http://127.0.0.1:8000

## Tests & Lint
```bash
python manage.py test
ruff check .
flake8
npx eslint static/js --ext .js
```

## Production
- Set `DJANGO_SETTINGS_MODULE=premium_portfolio.settings.prod`
- Configure `DJANGO_SECRET_KEY`, `ALLOWED_HOSTS`, email settings, and GA/Recaptcha as needed
- Run `python manage.py collectstatic`
- Use `Procfile` or Dockerfile to deploy (Heroku‑like platforms, Fly.io, Render, etc.)

## Docker
```bash
docker build -t premium-portfolio .
docker run -p 8000:8000 --env-file .env premium-portfolio
```

## Analytics & Privacy
- GA loads only after consent. Set `GA_MEASUREMENT_ID` to enable.
- Update `templates/includes/consent.html` copy as needed.

## Security & CSP
- Example CSP header included in `portfolio/middleware.py`. Adjust sources to match your assets.
- Keep `SecurityMiddleware` enabled and set secure cookie flags in prod settings.

## SEO & Performance
- Critical CSS inlined in `base.html`
- Preconnect/preload Google Fonts
- Lazy-loading images; responsive images placeholders in `static/images/README.md`

## Sitemap & Robots
- `/sitemap.xml` is dynamic (projects, posts, static pages)
- `/robots.txt` dynamic includes sitemap URL

## Resume PDF
- Put your resume at `static/resume/resume.pdf`. A placeholder README is provided.

## Environment Variables
- DJANGO_SECRET_KEY, ALLOWED_HOSTS, GA_MEASUREMENT_ID, RECAPTCHA_SITE_KEY/SECRET_KEY
- EMAIL_* for SMTP in production

## Future Enhancements
- Image optimization pipeline and CDN
- A/B testing and experiments framework
- Caching for search index and pages