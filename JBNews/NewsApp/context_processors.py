# NewsApp/context_processors.py

from .models import Category, SiteContact, Advertisement
from django.db import models as db_models
from django.utils import timezone


def base_context(request):
    all_cats = list(Category.objects.all())
    return {
        "nav_categories":      Category.objects.filter(show_in_nav=True),
        "dropdown_categories": Category.objects.all(),
        "footer_cats_col1":     all_cats[:5],    # first 5
        "footer_cats_col2":     all_cats[5:10],
        "site_contact":        SiteContact.get(),
    }


def base_context(request):
    # Get one active ad per placement
    def get_ad(placement):
        return (
            Advertisement.objects
            .filter(placement=placement, is_active=True)
            .filter(
                db_models.Q(starts_at__isnull=True) | db_models.Q(
                    starts_at__lte=timezone.now().date())
            )
            .filter(
                db_models.Q(ends_at__isnull=True) | db_models.Q(
                    ends_at__gte=timezone.now().date())
            )
            .order_by("?")          # random ad from available pool
            .first()
        )

    return {
        "nav_categories":       Category.objects.filter(show_in_nav=True),
        "dropdown_categories":  Category.objects.all(),
        "site_contact":         SiteContact.get(),
        "footer_cats_col1":     list(Category.objects.all())[:5],
        "footer_cats_col2":     list(Category.objects.all())[5:10],
        "ad_sidebar_main":    get_ad(Advertisement.Placement.SIDEBAR_MAIN),
        "ad_sidebar_small_1": get_ad(Advertisement.Placement.SIDEBAR_SMALL_1),
        "ad_sidebar_small_2": get_ad(Advertisement.Placement.SIDEBAR_SMALL_2),
    }
