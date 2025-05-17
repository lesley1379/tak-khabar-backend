from django.db import models
from django.urls import reverse
from django.utils import timezone
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from mptt.fields import TreeForeignKey
from django.conf import settings


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام تگ")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag_posts', args=[self.slug])


class Category(MPTTModel):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")
    description = models.TextField(verbose_name="توضیحات", blank=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="دسته‌بندی والد"
    )

    class MPTTMeta:
        order_insertion_by = ['name']
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_articles', args=[self.slug])


def blog_image_path(instance, filename):
    # تصاویر در مسیر blog_images/سال/ماه/ذخیره می‌شوند
    return f'blog_images/{instance.publish_date.year}/{instance.publish_date.month}/{filename}'


class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'پیش‌نویس'),
        ('published', 'منتشر شده'),
        ('archived', 'بایگانی شده'),
    ]

    title = models.CharField(max_length=200, verbose_name="عنوان")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")
    summary = models.TextField(max_length=300, verbose_name="چکیده مطلب", blank=True)
    content = RichTextUploadingField(verbose_name="محتوا")
    source = models.CharField(max_length=200, verbose_name="منبع", blank=True, null=True)
    source_url = models.URLField(verbose_name="لینک منبع", blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='articles',
        verbose_name="نویسنده"
    )
    publish_date = models.DateTimeField(default=timezone.now, verbose_name="تاریخ انتشار")
    update_date = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    image = models.ImageField(upload_to=blog_image_path, verbose_name="تصویر شاخص")
    image_caption = models.CharField(max_length=200, verbose_name="عنوان تصویر", blank=True)
    tags = models.ManyToManyField(Tag, related_name='articles', verbose_name="تگ‌ها")
    categories = models.ManyToManyField('Category', related_name='articles', verbose_name="دسته‌بندی‌ها")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="وضعیت"
    )
    is_featured = models.BooleanField(default=False, verbose_name="مقاله ویژه")
    view_count = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")
    seo_title = models.CharField(max_length=60, verbose_name="عنوان سئو", blank=True)
    seo_description = models.CharField(max_length=160, verbose_name="توضیحات سئو", blank=True)

    class Meta:
        ordering = ['-publish_date']
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.slug])

    def get_image_url(self):
        if self.image:
            return self.image.url
        return '/static/assets/img/blog/default.jpg'

    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def save(self, *args, **kwargs):
        if not self.slug:  # فقط اگر slug وجود ندارد
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while Article.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

