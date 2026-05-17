from django.urls import path
from . import views

app_name = "news"
urlpatterns = [
    path("", views.HomepageView.as_view(), name="homepage"),
    # Article detail — /article/my-article-title/
    path(
        "article/<slug:slug>/",
        views.ArticleDetailView.as_view(),
        name="article_detail"
    ),

    # Category listing — /category/sports/
    path(
        "category/<slug:slug>/",
        views.CategoryView.as_view(),
        name="category"
    ),
    # urls.py — add to urlpatterns

    path("contact/", views.ContactView.as_view(), name="contact"),

    path("subscribe/",                views.subscribe,
         name="subscribe"),
    path("unsubscribe/<uuid:token>/",
         views.unsubscribe,               name="unsubscribe"),
    # urls.py

    path("search/", views.search, name="search"),
    # urls.py

    path("ad/click/<int:ad_id>/", views.ad_click, name="ad_click"),
]
