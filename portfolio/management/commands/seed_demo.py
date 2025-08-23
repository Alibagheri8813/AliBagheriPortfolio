from django.core.management.base import BaseCommand
from django.utils import timezone
from portfolio.models import Tag, Project, ProjectImage, BlogPost, Testimonial, Skill

class Command(BaseCommand):
    help = "Seed demo content (projects, posts, testimonials, skills)."

    def handle(self, *args, **options):
        tags = ["web", "ui-ux", "ai", "mobile", "branding", "open-source"]
        tag_objs = {t: Tag.objects.get_or_create(name=t.title(), slug=t)[0] for t in tags}

        projects = [
            ("NeuraNews – AI Summaries", "Cutting-edge summarizer", ["ai", "web"]),
            ("Minty – Finance App", "Modern money manager", ["mobile", "ui-ux"]),
            ("LumenSite – Static Engine", "Ultra-fast static engine", ["open-source", "web"]),
            ("NovaBrand – Identity", "Visual identity system", ["branding", "ui-ux"]),
            ("PixelPress – Blog Kit", "Elegant blogging toolkit", ["open-source", "web"]),
            ("FlowBoard – Kanban", "Minimal kanban for teams", ["web", "ui-ux"]),
        ]
        for idx, (title, summary, tgs) in enumerate(projects, start=1):
            p, _ = Project.objects.get_or_create(
                slug=title.lower().replace(" ", "-"),
                defaults=dict(
                    title=title,
                    summary=summary,
                    content="## Case Study\n\nChallenge...\n\nSolution...",
                    roles="Designer, Developer",
                    tools="Django, JS, CSS",
                    challenge="Describe the challenge...",
                    solution="Describe the solution...",
                    metrics="• +35% conversion\n• 1.2s LCP",
                    hero_image_url=f"/static/img/placeholder{idx}.svg",
                    featured=idx <= 3,
                    published=timezone.now(),
                )
            )
            p.tags.set([tag_objs[t] for t in tgs])
            ProjectImage.objects.get_or_create(project=p, image_url=f"/static/img/placeholder{idx}.svg", caption="Overview")

        posts = [
            ("Designing delightful onboarding", "Onboarding that respects attention."),
            ("A tiny guide to web performance", "Fast enough to feel instant."),
            ("Writing maintainable CSS", "Scale your CSS without tears."),
            ("Accessible by default", "Make it work for everyone."),
            ("Learning in public", "Grow faster by sharing."),
            ("From idea to shipped", "Shipping beats perfection."),
        ]
        for idx, (title, summary) in enumerate(posts, start=1):
            post, _ = BlogPost.objects.get_or_create(
                slug=title.lower().replace(" ", "-"),
                defaults=dict(
                    title=title,
                    summary=summary,
                    content_markdown="# " + title + "\n\n" + ("Lorem ipsum " * 120),
                    published=timezone.now(),
                )
            )
            post.tags.set([tag_objs["web"]])

        for t in [
            ("Sam Patel", "Founder, NeuraNews", "Alex is meticulous and fast."),
            ("Jamie Lee", "PM, Minty", "10/10 execution from idea to polish."),
            ("Ava Brooks", "CTO, LumenSite", "Clean code and smart tradeoffs."),
            ("Marco Díaz", "Brand Lead", "Premium visuals that convert."),
            ("Taylor Kim", "Team Lead", "Great partner under pressure."),
        ]:
            Testimonial.objects.get_or_create(author_name=t[0], role=t[1], content=t[2])

        for s in [
            ("Python", 90, "Engineering"),
            ("Django", 90, "Engineering"),
            ("JavaScript", 85, "Engineering"),
            ("CSS", 88, "Design"),
            ("Figma", 86, "Design"),
            ("React", 75, "Engineering"),
            ("Accessibility", 80, "Quality"),
            ("SEO", 78, "Quality"),
            ("Perf Tuning", 82, "Quality"),
            ("UX Writing", 70, "Design"),
        ]:
            Skill.objects.get_or_create(name=s[0], defaults={"proficiency": s[1], "category": s[2]})

        self.stdout.write(self.style.SUCCESS("Demo content seeded."))