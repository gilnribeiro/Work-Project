import scrapy
from ..items import NetEmpregosItem
from itemloaders import ItemLoader
from scrapy.selector import Selector
from datetime import date
from urllib.parse import urljoin

class NetEmpregosSpider(scrapy.Spider):
    name = 'net_empregos'
    # allowed_domains = ['https://www.net-empregos.com/pesquisa-empregos.asp?chaves=&cidade=&categoria=0&zona=0&tipo=0']
    start_urls = [
        'https://www.net-empregos.com/pesquisa-empregos.asp?chaves=&cidade=&categoria=0&zona=0&tipo=0'
        ]

    def parse(self, response):
        sel = Selector(response)
    
        for href in response.css('.align-self-center a::attr(href)').getall():    
            url = response.urljoin(href)
            yield scrapy.Request(url, callback = self.parse_contents)

        next_page = sel.css('.text-center nav a::attr(href)').extract()[-1]
        if next_page is not None:
            url = urljoin('https://www.net-empregos.com', next_page)
            yield scrapy.Request(url, callback=self.parse)


    def parse_contents(self, response):
        il = ItemLoader(item=NetEmpregosItem(), selector=response)
        il.add_css('job_description', 'p')
        il.add_css('job_title', '.title')
        il.add_css('post_date', '.candidate-listing-footer li:nth-child(3)')
        il.add_value('scrape_date', date.today().strftime("%d/%m/%Y"))
        il.add_css('company', '.flaticon-work+ a')
        il.add_css('job_location', '.flaticon-pin+ a')
        il.add_css('job_category', '.fa-tags+ a')
        il.add_value('job_href', str(response.url))

        yield il.load_item()

