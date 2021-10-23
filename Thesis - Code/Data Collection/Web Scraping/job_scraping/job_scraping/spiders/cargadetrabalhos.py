import scrapy
from .items import JobVacancyItem
from itemloaders import ItemLoader
from scrapy.selector import Selector
from datetime import date
from urllib.parse import urljoin

class CargaDeTrabalhosSpider(scrapy.Spider):
    name = 'cargadetrabalhos'
    start_urls = [
        'http://www.cargadetrabalhos.net/category/uncategorized/page/1/?submit=pesquisar%20categoria'
        ]
    
    custom_settings = {
        f'{name}.json': {
        'format': 'jsonlines',
        'encoding': 'utf8',
        # 'store_empty': False,
        # 'fields': ['job_title', 'job_description', 'post_date', 'scrape_date', 'company',
        #            'job_location', 'job_category', 'job_href', 'salary'], 
        }
    }

    def parse(self, response):
        sel = Selector(response)
        for job in response.css('.entrycontent'):
            il = ItemLoader(item=JobVacancyItem(), selector=job)
            il.add_css('job_description', 'p')
            il.add_css('job_title', 'h2 a')
            il.add_css('post_date', '.date')
            il.add_value('scrape_date', date.today().strftime("%d/%m/%Y"))
            il.add_css('company', 'b:nth-child(1)')
            il.add_css('job_location', 'b:nth-child(3)')
            il.add_value('job_category', '')
            il.add_css('job_href', 'h2 a::attr(href)')
            il.add_value('salary', '')

            yield il.load_item()

        next_page = sel.xpath('//*[@id="content"]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/a[2]/@href').get()
        if next_page is not None:
            # url = urljoin('http://www.cargadetrabalhos.net', next_page)
            yield scrapy.Request(next_page, callback=self.parse)
