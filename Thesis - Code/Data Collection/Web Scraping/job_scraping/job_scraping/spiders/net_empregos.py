# import scrapy
# from ..items import NetEmpregosItem
# from scrapy.loader import ItemLoader
# from datetime import date
# from urllib.parse import urljoin

# class NetEmpregosSpider(scrapy.Spider):
#     name = 'net_empregos'
#     # allowed_domains = ['https://www.net-empregos.com/pesquisa-empregos.asp?chaves=&cidade=&categoria=0&zona=0&tipo=0']
#     start_urls = [
#         'https://www.net-empregos.com/pesquisa-empregos.asp?chaves=&cidade=&categoria=0&zona=0&tipo=0'
#         ]


#     def parse(self, response):
        
#         next_page = response.css('.d-lg-none::attr(href)').get()
#         complete_url = 'https://www.net-empregos.com' + str(response.css('.d-lg-none::attr(href)').get())

#         for job in response.css('.media'):    
            
#             il = ItemLoader(item=NetEmpregosItem(), selector=job)

#             # il.add_value('job_href', 'https://www.net-empregos.com/pesquisa-empregos.asp?chaves=&cidade=&categoria=0&zona=0&tipo=0')

#             il.add_css('job_href', 'h2 a::attr(href)')

#             job_url = response.css('h2 a::attr(href)').get()
#             job_url = response.urljoin(job_url)
            
#             item = il.load_item()
    
#             scrapy.Request(job_url)

#             il = ItemLoader(item=item, selector=response)

#             il.add_css('job_description', 'p')
#             il.add_css('job_title', '.title')
#             il.add_css('post_date', '.candidate-listing-footer li:nth-child(3)')
#             il.add_value('scrape_date', date.today().strftime("%d/%m/%Y"))
#             il.add_css('company', '.flaticon-work+ a')
#             il.add_css('job_location', '.flaticon-pin+ a')
#             il.add_css('job_category', '.fa-tags+ a')

#             yield il.load_item()
        
#         if next_page is not None:
#             yield scrapy.Request(complete_url, callback=self.parse)

import scrapy
from scrapy.http.request import Request
from ..items import NetEmpregosItem
from scrapy.loader import ItemLoader
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
            
            # il = ItemLoader(item=NetEmpregosItem(), selector=job)

            # il.add_value('job_href', 'https://www.net-empregos.com')
            # il.add_css('job_href', 'h2 a::attr(href)')

            # item = il.load_item()
    
            # yield scrapy.Request(job_url)
            # job_url = sel.css('h2 a::attr(href)').get()
            url = response.urljoin(href)
            yield scrapy.Request(url, callback = self.parse_contents)

        next_page = sel.css('.text-center nav a::attr(href)').extract()[-1]
        # next_page = sel.xpath('//html/body/div[2]/div/div/div[2]/div[24]/nav/ul/li[5]/a[2]')
        if next_page is not None:
            url = urljoin('https://www.net-empregos.com', next_page)
            print('\n\n\n\n\n\n\n\n\n\n', url)
            yield scrapy.Request(url, callback=self.parse)
            # yield response.follow(next_page, callback=self.parse)


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

