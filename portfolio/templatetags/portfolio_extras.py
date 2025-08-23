from django import template
import markdown2
import bleach

register = template.Library()

ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS.union({"p", "pre", "span", "img", "h2", "h3", "h4", "blockquote", "code", "ul", "ol", "li"})
ALLOWED_ATTRS = {"img": ["src", "alt", "title", "loading", "decoding"], "*": ["class", "id"]}

@register.filter
def markdown_safe(value: str) -> str:
    html = markdown2.markdown(value or "", extras=["fenced-code-blocks", "tables"])
    return bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)

@register.filter
def reading_time(words: int) -> str:
    return f"{max(1, int(words))} min read"