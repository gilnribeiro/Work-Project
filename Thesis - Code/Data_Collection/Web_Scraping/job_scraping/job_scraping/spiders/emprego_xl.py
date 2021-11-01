import scrapy
from .items import JobVacancyItem
# from scrapy.loader import ItemLoader
from itemloaders import ItemLoader
from scrapy.selector import Selector
from datetime import date
import datetime as dt
from w3lib.html import remove_tags


def converToDatetime(x, year=' 2021'):
    x += year
    return dt.datetime.strptime(x, '%d %b %Y')


class EmpregoXlSpider(scrapy.Spider):
    name = 'emprego_xl'
    start_urls = [
        'https://www.empregoxl.com/empregos?p=1'
        ]
    
    def parse(self, response):
        sel = Selector(response)
    
        # for job in response.css('.joblisting a::attr(href)').getall():  
        for job in response.css('.joblisting a'):
            href = job.css('::attr(href)').get()
            last_date = converToDatetime(remove_tags(job.css('.date').get()))

            # il = ItemLoader(item=JobVacancyItem(), selector=response)
            # il.add_css('post_date', '.date')
            
            # item = il.load_item()
            url = response.urljoin(href)
            yield scrapy.Request(url, callback = self.parse_contents)

        # Scrape only until one week post results
        today = dt.datetime.today()
        delta = today - last_date
        if delta.days <= 7:
            next_page = sel.css('#paginacao a::attr(href)')[-1].get()
            if next_page is not None and next_page != response.url:
                yield scrapy.Request(next_page, callback=self.parse)


    def parse_contents(self, response):
        # item = response.meta['item']
        il = ItemLoader(item=JobVacancyItem(), selector=response)
        il.add_css('job_description', '#description')
        il.add_css('job_title', 'h2')
        il.add_css('post_date', 'a~ strong')
        il.add_css('post_date', 'p > strong~ strong')
        il.add_value('scrape_date', date.today().strftime("%d/%m/%Y"))
        il.add_value('job_category', '')
        il.add_css('job_location', 'span strong')  
        il.add_css('company', 'p > .fading+ strong')
        il.add_value('job_href', str(response.url))
        il.add_value('salary', '')

        yield il.load_item()
