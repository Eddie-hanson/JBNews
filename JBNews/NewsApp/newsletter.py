# NewsApp/newsletter.py

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import NewsletterSubscriber


def send_newsletter(article, request):
    """
    Called automatically when an article is published.
    Sends an email to all active subscribers.
    """
    subscribers = NewsletterSubscriber.objects.filter(is_active=True)

    if not subscribers.exists():
        return

    # Build the excerpt — use article.excerpt or first 30 words of write_up
    if article.excerpt:
        excerpt = article.excerpt
    else:
        words = article.write_up.split()
        excerpt = " ".join(words[:30]) + ("..." if len(words) > 30 else "")

    # Full URL to the article
    article_url = request.build_absolute_uri(
        f"/article/{article.slug}/"
    )

    # Full URL to the article picture
    article_picture_url = request.build_absolute_uri(
        article.picture.url
    )

    for subscriber in subscribers:
        unsubscribe_url = request.build_absolute_uri(
            f"/unsubscribe/{subscriber.token}/"
        )

        html_content = render_to_string("emails/newsletter.html", {
            "article":             article,
            "article_excerpt":     excerpt,
            "article_url":         article_url,
            "article_picture_url": article_picture_url,
            "unsubscribe_url":     unsubscribe_url,
        })

        msg = EmailMultiAlternatives(
            subject=f"[JBNews] {article.title}",
            # plain text fallback
            body=f"{article.title}\n\n{excerpt}\n\nRead more: {article_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber.email],
        )
        msg.attach_alternative(html_content, "text/html")

        try:
            msg.send()
        except Exception as e:
            # Log the error but don't crash — keep sending to other subscribers
            print(f"Failed to send to {subscriber.email}: {e}")
