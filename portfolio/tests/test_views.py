from django.test import TestCase
from django.urls import reverse
from portfolio.models import Project, BlogPost, Tag, ContactSubmission

class ViewsTests(TestCase):
    def setUp(self):
        t = Tag.objects.create(name="Web", slug="web")
        self.p = Project.objects.create(title="Test Project", slug="test-project", summary="S")
        self.p.tags.add(t)
        self.b = BlogPost.objects.create(title="Test Post", slug="test-post", summary="S", content_markdown="Hello")

    def test_home_ok(self):
        r = self.client.get(reverse("home"))
        self.assertEqual(r.status_code, 200)

    def test_project_detail(self):
        r = self.client.get(self.p.get_absolute_url())
        self.assertEqual(r.status_code, 200)

    def test_blog_detail(self):
        r = self.client.get(self.b.get_absolute_url())
        self.assertEqual(r.status_code, 200)

    def test_search_api(self):
        r = self.client.get(reverse("search_api"), {"q": "Test"})
        self.assertEqual(r.status_code, 200)
        self.assertIn("projects", r.json())

    def test_contact_ajax(self):
        r = self.client.post(reverse("contact"), {
            "name": "A", "email": "a@b.com", "message": "Hi"
        }, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(ContactSubmission.objects.exists())