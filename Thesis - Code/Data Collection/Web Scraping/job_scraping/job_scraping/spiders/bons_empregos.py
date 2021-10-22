import scrapy
from .items import JobVacancyItem
from itemloaders import ItemLoader
from scrapy.selector import Selector
from datetime import date
from urllib.parse import urljoin

class BonsEmpregosSpider(scrapy.Spider):
    name = 'bons_empregos'
    start_urls = [
        'https://www.bonsempregos.com/procurar-emprego'
        ]

    def parse(self, response):
        sel = Selector(response)
    
        for href in response.css('.tituloemprego a::attr(href)').getall():  

            il = ItemLoader(item=JobVacancyItem(), selector=response)
            il.add_css('job_location', '.categoriasemprego a:nth-child(1)')  
            il.add_css('job_category', 'a+ a')
            item = il.load_item()
            url = response.urljoin(href)
            yield scrapy.Request(url, callback = self.parse_contents, meta={'item':item})

        next_page = sel.css('#block-system-main .last a::attr(href)').get()
        if next_page is not None:
            url = urljoin('https://www.bonsempregos.com', next_page)
            yield scrapy.Request(url, callback=self.parse)


    def parse_contents(self, response):
        item = response.meta['item']
        il = ItemLoader(item=item, selector=response)
        il.add_css('job_description', '.anuncio')
        il.add_css('job_title', '.page-header')
        il.add_css('post_date', '.validadedoemprego', re = '(\d{1,2}?\s\w{3,9}?,\s\d{4}?)')
        il.add_value('scrape_date', date.today().strftime("%d/%m/%Y"))
        il.add_css('job_category', '.odd:nth-child(1) .col2')
        il.add_css('company', '.sobreempresa ::text', re='([a-zA-z]\w{3,30})')
        il.add_value('job_href', str(response.url))
        il.add_value('salary', '')

        yield il.load_item()

     