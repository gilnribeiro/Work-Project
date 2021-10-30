import scrapy
from .items import JobVacancyItem
from itemloaders import ItemLoader
from scrapy.selector import Selector
from datetime import date, timedelta
import datetime as dt
from urllib.parse import urljoin
from w3lib.html import remove_tags
import re


def longToShortDate(x, sep):
    months = ['janeiro', 'fevereiro','março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
    months_dic = {value:idx+1 for idx, value in enumerate(months)}
    date = [i.strip() for i in x.split(sep)]
    return f'{date[0]}/{months_dic[date[1]]}/{date[2]}'

# convert to datetime object
def convertToDatetime(x, function=longToShortDate):
    x = x.lower().replace(',','')
    x = dt.datetime.strptime(function(x, ' '), "%d/%m/%Y")
    return x


class BonsEmpregosSpider(scrapy.Spider):
    name = 'bons_empregos'
    start_urls = [
        'https://www.bonsempregos.com/procurar-emprego'
        ]

    def __init__(self):
        self.last_date = dt.datetime.today() - timedelta(days=7)

    def parse(self, response):
        sel = Selector(response)
    
        for href in response.css('.tituloemprego a::attr(href)').getall():  

            il = ItemLoader(item=JobVacancyItem(), selector=response)
            il.add_css('job_location', '.categoriasemprego a:nth-child(1)')  
            il.add_css('job_category', 'a+ a')
            item = il.load_item()
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_contents, meta={'item':item})

        # Scrape only until one week post results
        today = dt.datetime.today()
        delta = today - self.last_date
        if delta.days <= 7:
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
        # il.add_css('job_category', '.views-field-nothing a:nth-child(2)')
        il.add_css('company', '.sobreempresa ::text', re='([a-zA-z]\w{3,30})')
        il.add_value('job_href', str(response.url))
        il.add_value('salary', '')

        # Get last date
        text = remove_tags(response.css('.validadedoemprego').get())
        self.last_date = convertToDatetime(re.search('(\d{1,2}?\s\w{3,9}?,\s\d{4}?)', text).group())

        yield il.load_item()

     