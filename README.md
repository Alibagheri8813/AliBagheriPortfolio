# Premium Portfolio (Django 5)

Modern, premium portfolio for a high‑performing creator with projects, blog, resume (print-to-PDF), case study modals (deep-linkable), AJAX contact with rate limit, SEO (OpenGraph/Twitter/JSON-LD), analytics consent, dark mode, accessibility, and strong performance.

## Features
- Projects grid, tags, filters, deep‑linkable case study modals with SSR fallback
- Blog with reading time, tags, SEO metadata, JSON‑LD
- Resume page with print‑to‑PDF export
- About, testimonials, contact (AJAX + CSRF + basic rate limiting + reCAPTCHA stub)
- Dynamic `sitemap.xml`, `robots.txt`, canonical tags, OpenGraph/Twitter cards
- Performance: critical CSS inline, preconnect/preload, lazy images, deferred JS
- A11y: semantic HTML, labeled forms, keyboard support, prefers‑reduced‑motion
- Security: CSRF, safe templates, optional CSP header
- CI: Python ruff, ESLint, Django tests
- Dockerfile, Procfile

## Quickstart
1. python -m venv .venv && source .venv/bin/activate
2. pip install -r requirements.txt
3. cp .env.example .env  # adjust as needed
4. python manage.py migrate
5. python manage.py seed_demo
6. python manage.py runserver
7. Visit http://127.0.0.1:8000

## Environment variables
- DJANGO_SECRET_KEY, DJANGO_DEBUG, ALLOWED_HOSTS, SITE_NAME, SITE_DOMAIN
- EMAIL_* (for prod): email backend; dev uses console backend
- DATABASE_URL (prod Postgres), GA_MEASUREMENT_ID
- RECAPTCHA_SITE_KEY, RECAPTCHA_SECRET_KEY (leave empty to disable verification)
- CSP_ENABLED=1 to enable example CSP header

## Dev scripts
- Python lint: ruff check .
- JS lint: npm install && npm run lint
- Tests: python manage.py test

## Deployment
- Docker: docker build -t portfolio . && docker run -p 8000:8000 --env-file .env portfolio
- Procfile (Heroku-like): web dyno via gunicorn
- Set DJANGO_SETTINGS_MODULE=premium_portfolio.settings.prod and configure DATABASE_URL/EMAIL_*

## Assets
- Replace SVG placeholders in `portfolio/static/img/` with real images (use responsive `<img srcset>`). Keep weights optimized, use lazy loading.
- Replace `icons/favicon.svg` as needed. Update `site.webmanifest`.

## Analytics consent
- Add your GA ID to `.env` (GA_MEASUREMENT_ID). Analytics only loads after consent.

## reCAPTCHA
- Add site/secret keys to `.env`. Verification disabled if keys are empty.

## Security
- Review and harden CSP in `portfolio/middleware.py`. Enable via CSP_ENABLED=1.
- Set secure cookie and HSTS in prod settings.

## Maintenance checklist
- Rotate SECRET_KEY; configure ALLOWED_HOSTS and HTTPS
- Attach CDN for static/media; image optimization pipeline (thumbor/imgproxy)
- Add caching (Redis), per-view/page cache for heavy pages
- Add sitemap ping on new posts; A/B testing hooks
- Monitor with Sentry (integrate DSN in prod)