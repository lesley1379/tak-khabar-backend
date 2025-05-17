from datetime import time
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from news.models import Article, Tag, Category
from users.models import User
import time

class ModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testauthor',
            password='testpass123',
            role='author'
        )
        self.tag = Tag.objects.create(name='سیاسی', slug='political')
        self.category = Category.objects.create(name='اقتصاد', slug='economy')

    def test_create_article(self):
        """تست ایجاد مقاله جدید"""
        article = Article.objects.create(
            title='عنوان تستی',
            content='محتوای تستی',
            author=self.user
        )
        article.tags.add(self.tag)
        article.categories.add(self.category)

        self.assertEqual(str(article), 'عنوان تستی')
        self.assertEqual(article.tags.count(), 1)
        self.assertEqual(article.status, 'draft')


class ArticleAPITests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.author = User.objects.create_user(
            username='author',
            password='password123',
            role='author'
        )
        self.regular_user = User.objects.create_user(
            username='regular',
            password='password123',
            role='user'
        )
        self.tag = Tag.objects.create(name='ورزشی', slug='sport')
        self.category = Category.objects.create(name='فرهنگی', slug='culture')

        unique_id = str(time.time()).replace('.', '')[-8:]
        self.valid_data = {
            'title': f'مقاله جدید {unique_id}',
            'content': 'محتوای مقاله جدید',
            'tags': ['sport'],
            'categories': ['culture']
        }

        self.article = Article.objects.create(
            title=f'مقاله موجود {unique_id}',
            content='محتوای موجود',
            author=self.author,
            slug=f'article-{unique_id}'
        )
        self.article.tags.add(self.tag)
        self.article.categories.add(self.category)

    def test_unauthenticated_access(self):
        url = reverse('article-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_article_as_author(self):
        self.client.force_authenticate(user=self.author)
        url = reverse('article-list')
        response = self.client.post(url, self.valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 2)
        self.assertIn('مقاله جدید', self.valid_data['title'])

    def test_create_article_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('article-list')
        response = self.client.post(url, self.valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_publish_action(self):
        self.client.force_authenticate(user=self.author)
        url = reverse('article-publish', kwargs={'pk': self.article.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, 'published')

    def test_archive_action(self):
        self.article.status = 'published'
        self.article.save()

        self.client.force_authenticate(user=self.author)
        url = reverse('article-archive', kwargs={'pk': self.article.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, 'archived')


class TagCategoryAPITests(APITestCase):

    def setUp(self):
        self.tag = Tag.objects.create(name='اجتماعی', slug='social')
        self.category = Category.objects.create(name='علمی', slug='science')

    def test_tag_list(self):
        url = reverse('tag-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'اجتماعی')

    def test_category_detail(self):
        url = reverse('category-detail', kwargs={'slug': 'science'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'علمی')