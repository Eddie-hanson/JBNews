# NewsApp/newsletter.py

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import NewsletterSubscriber


def send_newsletter(article):
    subscribers = NewsletterSubscriber.objects.filter(is_active=True)

    if not subscribers.exists():
        return

    # Build excerpt
    if article.excerpt:
        excerpt = article.excerpt
    else:
        words = article.write_up.split()
        excerpt = " ".join(words[:30]) + ("..." if len(words) > 30 else "")

    # Build URLs using SITE_URL from settings instead of request
    site_url = settings.SITE_URL.rstrip("/")
    article_url = f"{site_url}/article/{article.slug}/"
    picture_url = f"{site_url}{article.picture.url}" if article.picture else ""

    for subscriber in subscribers:
        unsubscribe_url = f"{site_url}/unsubscribe/{subscriber.token}/"

        html_content = render_to_string("emails/newsletter.html", {
            "article":             article,
            "article_excerpt":     excerpt,
            "article_url":         article_url,
            "article_picture_url": picture_url,
            "unsubscribe_url":     unsubscribe_url,
        })

        msg = EmailMultiAlternatives(
            subject=f"[JBNews] {article.title}",
            body=f"{article.title}\n\n{excerpt}\n\nRead more: {article_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber.email],
        )
        msg.attach_alternative(html_content, "text/html")

        try:
            msg.send()
            print(f"Newsletter sent to {subscriber.email}")
        except Exception as e:
            print(f"Failed to send to {subscriber.email}: {e}")
