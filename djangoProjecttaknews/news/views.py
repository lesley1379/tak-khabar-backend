from django.db.models import Q
from rest_framework import viewsets, filters, status, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Article, Tag, Category
from .serializers import *
from .filters import ArticleFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins
from users.views import AuthorOnlyPermission


class ArticleViewSet(viewsets.ModelViewSet):
    """
       list:
       دریافت لیست مقالات با امکان فیلتر، جستجو و مرتب‌سازی

       پارامترهای قابل استفاده:
       - search: جستجو در عنوان، چکیده و محتوا
       - tags: فیلتر بر اساس تگ‌ها (با اسلاگ)
       - categories: فیلتر بر اساس دسته‌بندی‌ها
       - status: فیلتر بر اساس وضعیت (draft, published, archived)
       - is_featured: فیلتر مقالات ویژه
       - ordering: مرتب‌سازی (publish_date, view_count)

       create:
       ایجاد مقاله جدید

       نیاز به احراز هویت دارد.
       فقط نویسندگان می‌توانند مقاله ایجاد کنند.

       retrieve:
       دریافت جزئیات یک مقاله

       update:
       به‌روزرسانی کامل مقاله

       نیاز به احراز هویت دارد.
       فقط نویسنده مقاله می‌تواند آن را به‌روزرسانی کند.

       partial_update:
       به‌روزرسانی جزئی مقاله

       نیاز به احراز هویت دارد.
       فقط نویسنده مقاله می‌تواند آن را به‌روزرسانی کند.

       destroy:
       حذف مقاله

       نیاز به احراز هویت دارد.
       فقط نویسنده مقاله می‌تواند آن را حذف کند.
       """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ArticleFilter
    search_fields = ['title', 'summary', 'content']
    ordering_fields = ['publish_date', 'view_count']
    ordering = ['-publish_date']

    def get_serializer_class(self):
        if self.action == 'create':
            return ArticleCreateSerializer
        elif self.action == 'retrieve':
            return ArticleDetailSerializer
        elif self.action == 'list':
            return ArticleListSerializer
        return ArticleSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'publish', 'archive']:
            return [permissions.IsAuthenticated(), AuthorOnlyPermission()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """
             انتشار مقاله

             تغییر وضعیت مقاله به 'published'
             نیاز به احراز هویت دارد.
             فقط نویسنده مقاله می‌تواند آن را منتشر کند.
             """
        article = self.get_object()
        article.status = 'published'
        article.save()
        return Response({'status': 'مقاله منتشر شد'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """
              بایگانی مقاله

              تغییر وضعیت مقاله به 'archived'
              نیاز به احراز هویت دارد.
              فقط نویسنده مقاله می‌تواند آن را بایگانی کند.
              """
        article = self.get_object()
        article.status = 'archived'
        article.save()
        return Response({'status': 'مقاله بایگانی شد'}, status=status.HTTP_200_OK)





class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
