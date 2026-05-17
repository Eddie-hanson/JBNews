# NewsApp/signals.py

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Article


# Store the previous status before save
@receiver(pre_save, sender=Article)
def store_previous_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._previous_status = Article.objects.get(
                pk=instance.pk
            ).status
        except Article.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None   # brand new article


# After save — send newsletter if status just flipped to PUBLISHED
@receiver(post_save, sender=Article)
def article_published_handler(sender, instance, created, **kwargs):
    previous = getattr(instance, "_previous_status", None)
    current = instance.status

    # Only send if it just became published — not on every save
    just_published = (
        current == Article.Status.PUBLISHED and
        previous != Article.Status.PUBLISHED
    )

    if just_published:
        from .newsletter import send_newsletter
        send_newsletter(instance)
