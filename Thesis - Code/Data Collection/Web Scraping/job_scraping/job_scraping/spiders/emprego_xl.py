import scrapy
from .items import JobVacancyItem
# from scrapy.loader import ItemLoader
from itemloaders import ItemLoader
from scrapy.selector import Selector
from datetime import date

class EmpregoXlSpider(scrapy.Spider):
    name = 'emprego_xl'
    start_urls = [
        'https://www.empregoxl.com/empregos?p=1'
        ]
    
    def parse(self, response):
        sel = Selector(response)
    
        for href in response.css('.joblisting a::attr(href)').getall():  
            url = response.urljoin(href)
            yield scrapy.Request(url, callback = self.parse_contents)

        next_page = sel.css('#paginacao a::attr(href)')[-1].get()
        if next_page is not None and next_page != response.url:
            yield scrapy.Request(next_page, callback=self.parse)


    def parse_contents(self, response):
        il = ItemLoader(item=JobVacancyItem(), selector=response)
        il.add_css('job_description', '#description')
        il.add_css('job_title', 'h2')
        il.add_css('post_date', 'p > strong~ strong')
        il.add_value('scrape_date', date.today().strftime("%d/%m/%Y"))
        il.add_value('job_category', '')
        il.add_css('job_location', 'span strong')  
        il.add_css('company', 'p > .fading+ strong')
        il.add_value('job_href', str(response.url))
        il.add_value('salary', '')

        yield il.load_item()
