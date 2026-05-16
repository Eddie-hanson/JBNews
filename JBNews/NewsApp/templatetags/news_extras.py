# NewsApp/templatetags/news_extras.py  ← create this file and folder

from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def time_ago(value):
    """
    - Under 60 mins  → X min ago
    - Under 24 hrs   → X hr ago
    - Under 7 days   → X days ago
    - 7 days+        → the actual date e.g. 10 May 2026
    """
    if not value:
        return ""

    now = timezone.now()
    diff = now - value
    secs = int(diff.total_seconds())
    mins = secs // 60
    hours = mins // 60
    days = diff.days

    if mins < 60:
        return f"{max(mins, 1)} min ago"
    elif hours < 24:
        return f"{hours} hr ago"
    elif days < 7:
        return f"{days} days ago"
    else:
        # %-d is Linux only — use lstrip("0") to remove leading zero on Windows too
        day = value.strftime("%d").lstrip("0")
        month = value.strftime("%b")
        year = value.strftime("%Y")
        return f"{day} {month} {year}"  # e.g. 10 May 2026
