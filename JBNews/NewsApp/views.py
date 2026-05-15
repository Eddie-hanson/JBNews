from django.shortcuts import render
# TODO:Replce dropdown with Category and make it dynamic from the backend
# TODO:Each news --> Title Cat write up date picture
# TODO:Create a page for read only where the link of an article leads to
#  that page so that a user can read the news
# TODO: The hompage will only show the picture and title with link embedded leading to the article
# TODO: Homepage will have a section that shows the news under various cat using a slider


# Create your views here.sss

from django.shortcuts import render


# news/views.py

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView
from django.db.models import Prefetch                      # ← was missing
from .models import Article, Category


# ─────────────────────────────────────────
# Homepage
# ─────────────────────────────────────────

class HomepageView(TemplateView):
    # ← matches your existing frontend
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # --- Section 1: Top Stories block ---
        # The one big breaking/important article (left, large picture)
        context["breaking_article"] = (
            Article.objects
            .filter(
                prominence=Article.Prominence.BREAKING,
                status=Article.Status.PUBLISHED
            )
            .first()
        )

        # The four supporting cards (right side)
        context["top_stories"] = (
            Article.objects
            .filter(
                prominence=Article.Prominence.TOP_STORY,
                status=Article.Status.PUBLISHED
            )
            .order_by("-published_at")[:4]
        )

        # --- Section 2: Featured category slider ---
        # Each category that has at least 1 featured published article,
        # with those articles pre-loaded so the template makes no extra queries
        context["featured_categories"] = (
            Category.objects
            .filter(
                articles__is_featured=True,
                articles__status=Article.Status.PUBLISHED
            )
            .prefetch_related(
                Prefetch(
                    "articles",
                    queryset=Article.objects.filter(
                        is_featured=True,
                        status=Article.Status.PUBLISHED
                    ).order_by("-published_at"),
                    to_attr="featured_articles",           # access as category.featured_articles
                )
            )
            .distinct()
        )

        # --- Navbar: all categories (for the dropdown) ---
        context["all_categories"] = Category.objects.all()

        return context


# ─────────────────────────────────────────
# Article detail (read-only page)
# ─────────────────────────────────────────

class ArticleDetailView(DetailView):
    model = Article
    # adjust to match your template folder
    template_name = "article_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        # Only published articles are publicly accessible
        return Article.objects.filter(status=Article.Status.PUBLISHED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Related articles: same category, exclude current, latest 4
        article = self.object
        if article.category:
            context["related_articles"] = (
                Article.objects
                .filter(
                    category=article.category,
                    status=Article.Status.PUBLISHED
                )
                .exclude(pk=article.pk)
                .order_by("-published_at")[:4]
            )
        else:
            context["related_articles"] = Article.objects.none()

        return context


# ─────────────────────────────────────────
# Category listing page
# ─────────────────────────────────────────

class CategoryView(TemplateView):
    # adjust to match your template folder
    template_name = "category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = get_object_or_404(Category, slug=self.kwargs["slug"])

        context["category"] = category
        context["articles"] = (
            Article.objects
            .filter(
                category=category,
                status=Article.Status.PUBLISHED
            )
            .order_by("-published_at")
        )
        # for navbar dropdown
        context["all_categories"] = Category.objects.all()

        return context


def contact(request):
    return render(request, 'contact.html')
