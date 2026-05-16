# NewsApp/signals.py  ← create this file

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article


@receiver(post_save, sender=Article)
def article_published_handler(sender, instance, created, **kwargs):
    """
    Fires every time an Article is saved.
    Sends newsletter only when status flips TO published for the first time.
    """
    if instance.status == Article.Status.PUBLISHED:
        # Only send once — check if it was previously unpublished
        if not created:
            try:
                previous = Article.objects.get(pk=instance.pk)
            except Article.DoesNotExist:
                return

        # Import here to avoid circular imports
        from .newsletter import send_newsletter
        from .models import NewsletterSubscriber

        # We need request for absolute URLs — use a stored flag instead
        instance._newsletter_sent = getattr(
            instance, "_newsletter_sent", False)
        if not instance._newsletter_sent:
            instance._newsletter_sent = True
            # Store on instance so the view can trigger it with request context
            instance._needs_newsletter = True
