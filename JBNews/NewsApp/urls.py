from django.urls import path
from . import views
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
    path("contact/", views.contact, name="contact"),
]
