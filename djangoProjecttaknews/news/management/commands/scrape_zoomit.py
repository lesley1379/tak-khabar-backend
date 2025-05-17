from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class Command(BaseCommand):
    help = 'Run Zoomit spider to scrape news articles'

    def handle(self, *args, **options):
        try:
            # تنظیمات Scrapy را دریافت می‌کند
            settings = get_project_settings()

            # تنظیمات اضافی (اختیاری)
            settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            settings.set('LOG_LEVEL', 'INFO')

            # ایجاد فرآیند Scrapy
            process = CrawlerProcess(settings)

            # اجرای اسپایدر zoomit
            process.crawl('zoomit')

            self.stdout.write(self.style.SUCCESS('Starting spider...'))
            process.start()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))