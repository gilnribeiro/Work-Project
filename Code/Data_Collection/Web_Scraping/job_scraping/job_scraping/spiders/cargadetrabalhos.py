import scrapy
from .items import JobVacancyItem
from itemloaders import ItemLoader
from scrapy.selector import Selector
from datetime import date
import datetime as dt
from w3lib.html import remove_tags


def longToShortDate(x, sep):
    months = ['Janeiro', 'Fevereiro','Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    months_dic = {value:idx+1 for idx, value in enumerate(months)}
    date = [i.strip() for i in x.split(sep)]
    return f'{date[0]}/{months_dic[date[1]]}/{date[2]}'

# convert to datetime object
def convertToDatetime(x, function=longToShortDate):
    x = x.lower().replace(',','')
    x = dt.datetime.strptime(function(x, '/'), "%d/%m/%Y")
    return x

    
class CargaDeTrabalhosSpider(scrapy.Spider):
    name = 'cargadetrabalhos'
    start_urls = [
        'https://www.cargadetrabalhos.net/page/1/'
        ]


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
            
            last_date = convertToDatetime(remove_tags(job.css('.date').get()))

            yield il.load_item()
    
        # Scrape only until one week post results
        today = dt.datetime.today()
        delta = today - last_date

        # if delta.days <= 7:
        next_page = sel.css('.next a::attr(href)').get()
        # next_page = sel.xpath('//*[@id="content"]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/a[2]/@href').get()
        if next_page is not None:
            # url = urljoin('http://www.cargadetrabalhos.net', next_page)
            yield scrapy.Request(next_page, callback=self.parse)
