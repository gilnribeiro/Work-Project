import scrapy
from .items import JobVacancyItem
from itemloaders import ItemLoader
from scrapy.selector import Selector
from datetime import date
import datetime as dt
from w3lib.html import remove_tags
from urllib.parse import urljoin

def converToDatetime(x):
    return dt.datetime.strptime(x.strip(), '%d-%m-%Y')

class NetEmpregosSpider(scrapy.Spider):
    name = 'net_empregos'
    # allowed_domains = ['https://www.net-empregos.com/pesquisa-empregos.asp?chaves=&cidade=&categoria=0&zona=0&tipo=0']
    start_urls = [
        'https://www.net-empregos.com/pesquisa-empregos.asp?categoria=0&zona=0&tipo=0'
        ]

    def parse(self, response, page=1):
        sel = Selector(response)
    
        # for href in response.css('.align-self-center a::attr(href)').getall(): 
        for job in response.css('.media'):
            href = job.css('a::attr(href)').get()
            last_date = converToDatetime(remove_tags(job.css('li:nth-child(1)').get()))
            url = response.urljoin(href)
            yield scrapy.Request(url, callback = self.parse_contents)

        max_page = int(response.css('.heading-2').get().split()[-1].split('<')[0])

        # Scrape only until one week post results
        today = dt.datetime.today()
        delta = today - last_date
        if delta.days <= 7:
            next_page = sel.css('.text-center nav a::attr(href)').extract()[-1]
            if next_page is not None:
                url = urljoin('https://www.net-empregos.com', next_page)
                page += 1
                if page == max_page:
                    return 'FINISH'
                yield scrapy.Request(url, callback=self.parse)

        # max_page = int(response.css('.heading-2').get().split()[-1].split('<')[0])
        # if page <= max_page:
        #     page += 1
        #     print(f'{page} RESULTS SCRAPED, {max_page-page} LEFT')
        #     next_page = f"https://www.net-empregos.com/pesquisa-empregos.asp?page={page}&categoria=0&zona=0&tipo=0"
        #     yield scrapy.Request(next_page, callback=self.parse)

    def parse_contents(self, response):
        il = ItemLoader(item=JobVacancyItem(), selector=response)
        il.add_css('job_description', 'p')
        il.add_css('job_title', '.title')
        il.add_css('post_date', '.candidate-listing-footer li:nth-child(3)')
        il.add_value('scrape_date', date.today().strftime("%d/%m/%Y"))
        il.add_css('company', '.flaticon-work+ a')
        il.add_css('job_location', '.flaticon-pin+ a')
        il.add_css('job_category', '.fa-tags+ a')
        il.add_value('job_href', str(response.url))
        il.add_value('salary', '')

        yield il.load_item()

