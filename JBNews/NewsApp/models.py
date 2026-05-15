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
