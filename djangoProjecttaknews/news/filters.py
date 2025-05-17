import django_filters
from django.db.models import Q
from .models import Article, Tag


class ArticleFilter(django_filters.FilterSet):
    """
       فیلترهای مقاله

       پارامترهای قابل استفاده:
       - tags: فیلتر بر اساس تگ‌ها (با اسلاگ)
       - categories: فیلتر بر اساس دسته‌بندی‌ها
       - status: فیلتر بر اساس وضعیت (draft, published, archived)
       - is_featured: فیلتر مقالات ویژه
       - search: جستجو در عنوان، چکیده و محتوا
       - exclude: حذف نتایج شامل کلمات خاص
       """
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
        label='تگ‌ها (بر اساس اسلاگ)'
    )

    search = django_filters.CharFilter(
        method='custom_search',
        label='جستجوی کلیدواژه'
    )

    exclude = django_filters.CharFilter(
        method='custom_exclude',
        label='حذف کلیدواژه'
    )

    class Meta:
        model = Article
        fields = ['tags', 'categories', 'status', 'is_featured']

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(summary__icontains=value) |
            Q(content__icontains=value)
        )

    def custom_exclude(self, queryset, name, value):
        return queryset.exclude(
            Q(title__icontains=value) |
            Q(summary__icontains=value) |
            Q(content__icontains=value)
        )