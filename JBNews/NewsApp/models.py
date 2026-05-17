import uuid
from django.db import models

# Create your models here.

# news/models.py

from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    show_in_nav = models.BooleanField(
        default=False,
        help_text="Tick to show this category in the navigation bar."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    class Prominence(models.TextChoices):
        NORMAL = "normal", "Normal"             # regular article
        TOP_STORY = "top_story", "Top Story"    # one of the 4 right-side cards
        BREAKING = "breaking", "Breaking News"

    # Core fields (from your TODOs)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True,
                            blank=True)   # used in the article URL
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="articles"
    )
    # full article body
    write_up = models.TextField()
    # short preview for homepage
    excerpt = models.TextField(blank=True, max_length=300)
    picture = models.ImageField(
        upload_to="articles/pictures/%Y/%m/")  # homepage thumbnail
    picture_caption = models.CharField(max_length=255, blank=True)
    # increments each time article is read
    views = models.PositiveIntegerField(default=0)
    # Dates
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Status & visibility
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT
    )

    # --- Homepage Section 1: Top Stories block ---
    prominence = models.CharField(
        max_length=10,
        choices=Prominence.choices,
        default=Prominence.NORMAL,
        help_text=(
            "Breaking = big left picture (only 1 active). "
            "Top Story = one of the 4 right cards (max 4 active)."
        )
    )

    # ---- Homepage Section 2: Category slider ----
    is_featured = models.BooleanField(
        # for homepage slider
        default=False, help_text="Include this article in the featured category slider.")

    class Meta:
        ordering = ["-published_at"]

    def clean(self):
        """Enforce the 1 breaking + 4 top_story limit at the model level."""
        if self.status != self.Status.PUBLISHED:
            return  # only enforce on published articles

        if self.prominence == self.Prominence.BREAKING:
            existing = Article.objects.filter(
                prominence=self.Prominence.BREAKING,
                status=self.Status.PUBLISHED
            ).exclude(pk=self.pk)
            if existing.exists():
                raise ValidationError(
                    "Only one Breaking News article can be active at a time. "
                    f'Currently: "{existing.first().title}"'
                )

        if self.prominence == self.Prominence.TOP_STORY:
            count = Article.objects.filter(
                prominence=self.Prominence.TOP_STORY,
                status=self.Status.PUBLISHED
            ).exclude(pk=self.pk).count()
            if count >= 4:
                raise ValidationError(
                    "Maximum of 4 Top Story articles allowed at a time."
                )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# models.py — add below Article model

class ContactMessage(models.Model):

    class Status(models.TextChoices):
        UNREAD = "unread",  "Unread"
        READ = "read",    "Read"
        REPLIED = "replied", "Replied"

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.UNREAD
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.subject} — {self.name} ({self.email})"


# models.py — add below ContactMessage

class SiteContact(models.Model):
    address = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    description = models.TextField(
        help_text="The paragraph shown under 'Get in Touch'"
    )

    # Social links — all optional
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    tiktok = models.URLField(blank=True)

    class Meta:
        verbose_name = "Site Contact Info"
        verbose_name_plural = "Site Contact Info"   # hides the default "s" in admin

    def __str__(self):
        return "Site Contact Info"

    def save(self, *args, **kwargs):
        # Enforce single row — always reuse pk=1
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        # Safe getter — returns the row or a blank default if not set up yet
        obj, _ = cls.objects.get_or_create(pk=1, defaults={
            "address":     "Not set",
            "email":       "not@set.com",
            "phone":       "Not set",
            "description": "Not set",
        })
        return obj


class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    # admin approves before showing
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.name} on {self.article.title}"


# models.py


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    # for unsubscribe link
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-subscribed_at"]

    def __str__(self):
        return self.email
