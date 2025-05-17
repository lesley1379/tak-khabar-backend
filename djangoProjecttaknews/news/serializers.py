from rest_framework import serializers
from .models import Article, Tag, Category


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ArticleSerializer(serializers.ModelSerializer):
    """
        سریالایزر اصلی مقاله

        فیلدها:
        - id: شناسه مقاله
        - title: عنوان مقاله
        - slug: اسلاگ مقاله
        - summary: چکیده مقاله
        - content: محتوای کامل مقاله (HTML)
        - source: منبع مقاله
        - source_url: لینک منبع
        - author: نویسنده مقاله
        - publish_date: تاریخ انتشار
        - update_date: تاریخ آخرین به‌روزرسانی
        - image: تصویر شاخص
        - image_caption: عنوان تصویر
        - tags: تگ‌های مقاله
        - categories: دسته‌بندی‌های مقاله
        - status: وضعیت مقاله
        - is_featured: آیا مقاله ویژه است؟
        - view_count: تعداد بازدیدها
        - seo_title: عنوان سئو
        - seo_description: توضیحات سئو
        - image_url: URL تصویر شاخص
        - status_display: نمایش متنی وضعیت
        """
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='slug',
        required=False
    )
    categories = serializers.SlugRelatedField(
        many=True,
        queryset=Category.objects.all(),
        slug_field='slug',
        required=False
    )

    class Meta:
        model = Article
        fields = '__all__'
        extra_kwargs = {
            'image': {'required': False},
            'status': {'default': 'draft'},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image_url'] = instance.get_image_url()
        representation['status_display'] = instance.get_status_display()
        return representation


class ArticleListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'summary', 'author',
            'publish_date', 'image_url', 'status', 'status_display',
            'is_featured', 'view_count', 'tags', 'categories'
        ]

    def get_image_url(self, obj):
        return obj.get_image_url()


class ArticleDetailSerializer(ArticleListSerializer):
    content = serializers.SerializerMethodField()

    class Meta(ArticleListSerializer.Meta):
        fields = ArticleListSerializer.Meta.fields + [
            'content', 'source', 'source_url',
            'seo_title', 'seo_description', 'update_date'
        ]

    def get_content(self, obj):
        return obj.content


class ArticleCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='slug',
        required=False
    )
    categories = serializers.SlugRelatedField(
        many=True,
        queryset=Category.objects.all(),
        slug_field='slug',
        required=False
    )

    class Meta:
        model = Article
        fields = [
            'title', 'summary', 'content', 'source', 'source_url',
            'author', 'image', 'image_caption', 'status', 'is_featured',
            'seo_title', 'seo_description', 'tags', 'categories'
        ]
        extra_kwargs = {
            'image': {'required': False},
            'status': {'default': 'draft'},
        }

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        categories_data = validated_data.pop('categories', [])

        article = Article.objects.create(**validated_data)

        for tag in tags_data:
            article.tags.add(tag)

        for category in categories_data:
            article.categories.add(category)

        return article
