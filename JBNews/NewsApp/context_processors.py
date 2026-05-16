# NewsApp/context_processors.py

from .models import Category, SiteContact


def base_context(request):
    all_cats = list(Category.objects.all())
    return {
        "nav_categories":      Category.objects.filter(show_in_nav=True),
        "dropdown_categories": Category.objects.all(),
        "footer_cats_col1":     all_cats[:5],    # first 5
        "footer_cats_col2":     all_cats[5:10],
        "site_contact":        SiteContact.get(),
    }
