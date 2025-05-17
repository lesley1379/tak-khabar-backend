import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse


class ZoomitSpider(scrapy.Spider):
    name = 'zoomit'
    start_urls = ['https://www.zoomit.ir/archive/']

    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'DOWNLOAD_DELAY': 2,
        'ROBOTSTXT_OBEY': False
    }

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def parse(self, response):
        self.driver.get(response.url)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.scroll-m-16"))
        )

        body = self.driver.page_source
        rendered_response = HtmlResponse(
            url=self.driver.current_url,
            body=body,
            encoding='utf-8'
        )

        links = rendered_response.css('div.scroll-m-16 a.sc-4c41eafb-6.fNLyDV::attr(href)').getall()
        for link in links[:15]:
            yield scrapy.Request(
                url=link,
                callback=self.parse_article
            )

    def parse_article(self, response):
        yield {
            'url': response.url,
            'title': response.css('h1::text').get('').strip(),
            'summary': response.css('span.sc-4c41eafb-5.lmthOZ::text').get('').strip(),
            'content': ' '.join(response.css('article p::text').getall()).strip(),
            'date': response.css('span.fa::text').get('').strip(),
            'comments': response.xpath('//svg[contains(@d, "M8 .5c2.078")]/following-sibling::span/text()').get(
                '0').strip()
        }

    def closed(self, reason):
        self.driver.quit()