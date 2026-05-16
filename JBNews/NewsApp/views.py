
# TODO:Replce dropdown with Category and make it dynamic from the backend
# TODO:Each news --> Title Cat write up date picture
# TODO:Create a page for read only where the link of an article leads to
#  that page so that a user can read the news
# TODO: The hompage will only show the picture and title with link embedded leading to the article
# TODO: Homepage will have a section that shows the news under various cat using a slider

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView
from django.db.models import Prefetch, F
from django.contrib import messages
from django.shortcuts import redirect
from .forms import ContactForm, CommentForm, NewsletterForm
from .models import ContactMessage, SiteContact, Article, Category, NewsletterSubscriber


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
        latest_published = Article.objects.filter(
            status=Article.Status.PUBLISHED
        ).order_by("-published_at")

        context["latest_main"] = latest_published.first()       # big left card
        # 5 smaller right items
        context["latest_list"] = latest_published[1:6]

        # --- Section 4: Popular News (1 featured left + 5 list right) ---
        popular_published = Article.objects.filter(
            status=Article.Status.PUBLISHED
            # most viewed first
        ).order_by("-views")

        context["popular_main"] = popular_published.first()      # big left card
        context["popular_list"] = popular_published[1:6]
        context["nav_categories"] = Category.objects.filter(show_in_nav=True)
        # --- Navbar: all categories (for the dropdown) ---
        context["all_categories"] = Category.objects.all()
        context["site_contact"] = SiteContact.get()

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

    def get_object(self):
        obj = super().get_object()
        # Increment view count every time the article page is opened
        Article.objects.filter(pk=obj.pk).update(views=F("views") + 1)
        obj.refresh_from_db()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Related articles: same category, exclude current, latest 4
        article = self.object
        # Related articles
        context["related_articles"] = (
            Article.objects
            .filter(category=article.category, status=Article.Status.PUBLISHED)
            .exclude(pk=article.pk)
            .order_by("-published_at")[:4]
        ) if article.category else Article.objects.none()

        # Approved comments + empty form
        context["comments"] = article.comments.filter(approved=True)
        context["comment_form"] = CommentForm()
        context["nav_categories"] = Category.objects.filter(show_in_nav=True)
        context["all_categories"] = Category.objects.all()
        context["site_contact"] = SiteContact.get()
        return context

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.save()
            messages.success(
                request, "Your comment has been submitted and is awaiting approval.")
            return redirect("news:article_detail", slug=article.slug)
        return render(request, "article_detail.html", {
            "object":          article,
            "comment_form":    comment_form,
            "comments":        article.comments.filter(approved=True),
            "related_articles": Article.objects.filter(
                category=article.category,
                status=Article.Status.PUBLISHED
            ).exclude(pk=article.pk).order_by("-published_at")[:4],
            "all_categories":  Category.objects.all(),
        })


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
        context["nav_categories"] = Category.objects.filter(show_in_nav=True)
        context["all_categories"] = Category.objects.all()
        context["site_contact"] = SiteContact.get()

        return context


class ContactView(TemplateView):
    template_name = "contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Prepopulate empty form on GET
        context["form"] = ContactForm()
        context["nav_categories"] = Category.objects.filter(show_in_nav=True)
        context["all_categories"] = Category.objects.all()
        context["site_contact"] = SiteContact.get()
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your message has been sent. We will get back to you shortly."
            )
            form = ContactForm()  # reset to empty form after success
        return render(request, "contact.html", {
            "form": form,
            "all_categories": Category.objects.all(),
        })


class ContactView(TemplateView):
    template_name = "contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ContactForm()
        context["site_contact"] = SiteContact.get()   # ← add this
        context["nav_categories"] = Category.objects.filter(show_in_nav=True)
        context["all_categories"] = Category.objects.all()
        context["site_contact"] = SiteContact.get()
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent.")
            form = ContactForm()
        return render(request, "contact.html", {
            "form":           form,
            "site_contact":   SiteContact.get(),        # ← add this
            "all_categories": Category.objects.all(),
        })


# views.py


def subscribe(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            # Re-activate if they previously unsubscribed
            obj, created = NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={"is_active": True}
            )
            if not created and not obj.is_active:
                obj.is_active = True
                obj.save()
                messages.success(
                    request, "Welcome back! You have been re-subscribed.")
            elif created:
                messages.success(
                    request, "You have successfully subscribed to our newsletter.")
            else:
                messages.info(request, "You are already subscribed.")
        else:
            messages.error(request, "Please enter a valid email address.")

    # Redirect back to whatever page they were on
    return redirect(request.META.get("HTTP_REFERER", "/"))


def unsubscribe(request, token):
    try:
        subscriber = NewsletterSubscriber.objects.get(token=token)
        subscriber.is_active = False
        subscriber.save()
        messages.success(request, "You have been unsubscribed successfully.")
    except NewsletterSubscriber.DoesNotExist:
        messages.error(request, "Invalid unsubscribe link.")
    return redirect("news:homepage")
