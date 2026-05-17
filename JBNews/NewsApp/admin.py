from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.db import models as db_models
from .models import Article, Category, ContactMessage, SiteContact, Comment, NewsletterSubscriber
from .newsletter import send_newsletter

# Register your models here.


# ─────────────────────────────────────────
# Category Admin
# ─────────────────────────────────────────

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "article_count", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at",)

    def article_count(self, obj):
        count = obj.articles.filter(status=Article.Status.PUBLISHED).count()
        return format_html('<b>{}</b> published', count)
    article_count.short_description = "Published Articles"


# ─────────────────────────────────────────
# Article Admin
# ─────────────────────────────────────────

class ProminenceFilter(admin.SimpleListFilter):
    title = "Homepage Slot"
    parameter_name = "prominence"

    def lookups(self, request, model_admin):
        return Article.Prominence.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(prominence=self.value())
        return queryset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    # ── List view ─────────────────────────
    list_display = (
        "title",
        "category",
        "status_badge",
        "prominence_badge",
        "is_featured",
        "published_at",
        "thumbnail_preview",
    )
    list_filter = (
        "status",
        ProminenceFilter,
        "is_featured",
        "category",
        "published_at",
    )
    search_fields = ("title", "excerpt", "write_up")
    list_editable = ("is_featured",)
    date_hierarchy = "published_at"
    ordering = ("-published_at",)

    # ── Detail/edit view ──────────────────
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = (
        "created_at",
        "updated_at",
        "thumbnail_preview",
        "homepage_slot_summary",
    )
    fieldsets = (
        ("Content", {
            "fields": ("title", "slug", "category", "write_up", "excerpt")
        }),
        ("Media", {
            "fields": ("picture", "thumbnail_preview", "picture_caption")
        }),
        ("Publishing", {
            "fields": ("status", "published_at")
        }),
        ("Homepage Placement", {
            "description": (
                "Breaking News = the large left picture (only 1 allowed). "
                "Top Story = one of the 4 right-side cards (max 4). "
                "Featured = appears in the category slider."
            ),
            "fields": ("prominence", "is_featured", "homepage_slot_summary")
        }),
        ("Timestamps", {
            "classes": ("collapse",),
            "fields":  ("created_at", "updated_at"),
        }),
    )

    # ── Actions ───────────────────────────
    actions = [
        "publish_articles",
        "publish_and_notify",
        "archive_articles",
        "mark_as_featured",
        "unmark_as_featured",
    ]

    @admin.action(description="Publish selected articles")
    def publish_articles(self, request, queryset):
        updated = queryset.update(
            status=Article.Status.PUBLISHED,
            published_at=timezone.now()
        )
        self.message_user(request, f"{updated} article(s) published.")

    @admin.action(description="Publish and send newsletter to subscribers")
    def publish_and_notify(self, request, queryset):
        count = 0
        for article in queryset:
            already_published = article.status == Article.Status.PUBLISHED
            if not already_published:
                article.status = Article.Status.PUBLISHED
                article.published_at = timezone.now()
                article.save()
                count += 1
            else:
                send_newsletter(article)
                count += 1
        self.message_user(request, f"Newsletter sent for {count} article(s).")

    @admin.action(description="Archive selected articles")
    def archive_articles(self, request, queryset):
        updated = queryset.update(status=Article.Status.ARCHIVED)
        self.message_user(request, f"{updated} article(s) archived.")

    @admin.action(description="Mark selected as Featured (slider)")
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f"{updated} article(s) marked as featured.")

    @admin.action(description="Remove selected from Featured (slider)")
    def unmark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(
            request, f"{updated} article(s) removed from featured.")

    def status_badge(self, obj):
        colours = {
            Article.Status.PUBLISHED: "#2e7d32",
            Article.Status.DRAFT:     "#f57c00",
            Article.Status.ARCHIVED:  "#757575",
        }
        colour = colours.get(obj.status, "#000")
        return format_html(
            '<span style="background:{colour};color:#fff;padding:2px 8px;'
            'border-radius:4px;font-size:11px;font-weight:600">{label}</span>',
            colour=colour,
            label=obj.get_status_display(),
        )
    status_badge.short_description = "Status"

    def prominence_badge(self, obj):
        icons = {
            Article.Prominence.BREAKING:  ("🔴", "#b71c1c"),
            Article.Prominence.TOP_STORY: ("🟡", "#e65100"),
            Article.Prominence.NORMAL:    ("⚪", "#555"),
        }
        icon, colour = icons.get(obj.prominence, ("⚪", "#555"))
        return format_html(
            '{icon} <span style="color:{colour};font-size:12px">{label}</span>',
            icon=icon,
            colour=colour,
            label=obj.get_prominence_display(),
        )
    prominence_badge.short_description = "Prominence"

    def thumbnail_preview(self, obj):
        if obj.picture:
            return format_html(
                '<img src="{}" style="height:60px;border-radius:4px;object-fit:cover;" />',
                obj.picture.url
            )
        return "No image"
    thumbnail_preview.short_description = "Preview"

    def homepage_slot_summary(self, obj):
        breaking_used = Article.objects.filter(
            prominence=Article.Prominence.BREAKING,
            status=Article.Status.PUBLISHED
        ).exclude(pk=obj.pk).exists()

        top_story_count = Article.objects.filter(
            prominence=Article.Prominence.TOP_STORY,
            status=Article.Status.PUBLISHED
        ).exclude(pk=obj.pk).count()

        return format_html(
            '<table style="font-size:13px;border-collapse:collapse">'
            '<tr><td style="padding:2px 12px 2px 0"><b>Breaking slot:</b></td>'
            '<td style="color:{b_colour}">{b_label}</td></tr>'
            '<tr><td style="padding:2px 12px 2px 0"><b>Top Story slots:</b></td>'
            '<td style="color:{t_colour}">{t_count}/4 used</td></tr>'
            '</table>',
            b_colour="#b71c1c" if breaking_used else "#2e7d32",
            b_label="TAKEN" if breaking_used else "Available",
            t_colour="#b71c1c" if top_story_count >= 4 else "#2e7d32",
            t_count=top_story_count,
        )
    homepage_slot_summary.short_description = "Homepage Slot Availability"

    @admin.register(ContactMessage)
    class ContactMessageAdmin(admin.ModelAdmin):
        list_display = ("name", "email", "subject", "status", "submitted_at")
        list_filter = ("status",)
        search_fields = ("name", "email", "subject", "message")
        readonly_fields = ("name", "email", "subject",
                           "message", "submitted_at")
        # mark read/replied directly from the list
        list_editable = ("status",)

    # admin.py — add this


@admin.register(SiteContact)
class SiteContactAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Contact Details", {
            "fields": ("description", "address", "email", "phone")
        }),
        ("Social Media Links", {
            "fields": ("twitter", "facebook", "linkedin", "instagram", "youtube", "tiktok"),
            "description": "Leave blank to hide that icon on the contact page."
        }),
    )

    def has_add_permission(self, request):
        # Prevent a second row from ever being created
        return not SiteContact.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion — always keep the one row
        return False


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "article", "approved", "created_at")
    list_filter = ("approved",)
    list_editable = ("approved",)   # approve/reject directly from the list
    search_fields = ("name", "email", "body")
    readonly_fields = ("name", "email", "body", "article", "created_at")


# admin.py — update ArticleAdmin


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "subscribed_at")
    list_filter = ("is_active",)
    search_fields = ("email",)
    list_editable = ("is_active",)    # activate/deactivate directly from list
    readonly_fields = ("token", "subscribed_at")
    actions = ["deactivate_subscribers"]

    @admin.action(description="Deactivate selected subscribers")
    def deactivate_subscribers(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} subscriber(s) deactivated.")
