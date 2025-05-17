# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ZoomitScraperPipeline:
    def process_item(self, item, spider):
        return item
from news.models import ScrapedArticle
from django.utils import timezone

class DjangoPipeline:
    def process_item(self, item, spider):
        if not ScrapedArticle.objects.filter(slug=item['slug']).exists():
            ScrapedArticle.objects.create(
                title=item['title'],
                slug=item['slug'],
                summary=item['summary'],
                content=item.get('content', ''),
                source_url=item['source_url'],
                publish_date=timezone.now(),  # یا تبدیل تاریخ از item
                image_url=item['image_url'],
                source='Zoomit',
                tags=', '.join(item.get('tags', [])))
        return item