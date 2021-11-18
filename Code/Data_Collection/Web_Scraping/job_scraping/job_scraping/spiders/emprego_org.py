from bs4 import BeautifulSoup
import scrapy
from .items import JobVacancyItem
# from scrapy.loader import ItemLoader
from itemloaders import ItemLoader
from scrapy.selector import Selector
from datetime import date, timedelta
import datetime as dt
from w3lib.html import remove_tags

def converToDatetime(x, year='2021'):
    if 'Hoje' in x:
        return dt.datetime.today()
    elif 'Ontem' in x:
        return dt.datetime.today() -  timedelta(days=1)
    else:
        date = x.split(' ')[1]+' '+x.split(' ')[0]
        date += ' '+year
        return dt.datetime.strptime(date, '%d-%b-%Y')

def get_jobDescription(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    ref = soup.find('div', {'id':'idviewjob'})

    jobCategory, salary, jobLocation, jobBenefits, postDate, company = '','','','','',''

    for i in ref.find_all('strong'):
        id = i.text
        if id == 'Categoria de Emprego:':
            try:
                jobCategory = i.parent.parent.find_all('td')[1].text.strip()
            except AttributeError:
                jobCategory = ''
        elif id == 'Remuneração:':
            try:
                salary = i.parent.parent.find_all('td')[1].text.strip()
            except AttributeError:
                salary = ''
        elif id == 'Localização do emprego:':
            try:
                jobLocation = i.parent.parent.find_all('td')[1].text.strip()
            except AttributeError:
                jobLocation = ''
        elif id == 'Benefícios e outras informações:':
            try:
                jobBenefits = i.parent.parent.find_all('td')[1].text.strip()
            except AttributeError:
                jobBenefits = ''
        elif id == 'Data de publicação:':
            try:
                postDate = i.parent.parent.find_all('td')[1].text.strip()
            except AttributeError:
                postDate = ''
        elif id == 'Empresa:':
            try:
                company = i.parent.parent.find_all('td')[1].text.strip()
            except AttributeError:
                company = ''


    dataToAdd = {'company': company, 'jobCategory': jobCategory, 'salary': salary,   
                'jobLocation': jobLocation, 'jobBenefits': jobBenefits, 'postDate': postDate}

    return dataToAdd
    

class EmpregoOrgSpider(scrapy.Spider):
    name = 'emprego_org'
    start_urls = [
        "https://empregos.org/jobfind.php?f=0&action=search&auth_sess=8cad55c8b89b646748e5876374404b30&ref=463aeeb6b3572f0d460e2c0da&bx_jtitle=&rdjt=2&jids[]=00&lids[]=000&bx_prv[]=&bx_plng[]=0&bx_kwd=&rdKeyw=2&bx_minsalary=&bx_maxsalary=&bx_lngids[]=-&rdLang=2&tids[]=0&posted=0&o=1&o_show=4&cmdSearch=++Pesquisar++"
        ]
    
    def parse(self, response, results=0):
        sel = Selector(response)
    
        # for href in response.css('h2 a::attr(href)').getall():  
        for job in response.css('.results'):
            # url = response.urljoin(href)
            href = job.css('h2 a::attr(href)').get()
            last_date = converToDatetime(remove_tags(job.css('.posted').get()))
            # il = ItemLoader(item=JobVacancyItem(), selector=response)
            # il.add_css('post_date', '.date')
            # item = il.load_item()
            url = href
            yield scrapy.Request(url, callback = self.parse_contents)

        # next_page = sel.css('form li~ .nolist+ .nolist a::attr(href)').get()
        # if next_page is not None and next_page != response.url:
        #     yield scrapy.Request(next_page, callback=self.parse)

        # Scrape only until one week post results
        today = dt.datetime.today()
        delta = today - last_date
        if delta.days <= 7:       
            max_results = int(response.css('.main_header h2').get().split('de')[-1].split(')')[0].strip())
            if results <= max_results:
                results += 50
                print(f'{results} RESULTS SCRAPED, {max_results-results} LEFT')
                next_page = f"https://empregos.org/jobfind.php?f={results}&action=search&auth_sess=8cad55c8b89b646748e5876374404b30&ref=463aeeb6b3572f0d460e2c0da&bx_jtitle=&rdjt=2&jids[]=00&lids[]=000&bx_prv[]=&bx_plng[]=0&bx_kwd=&rdKeyw=2&bx_minsalary=&bx_maxsalary=&bx_lngids[]=-&rdLang=2&tids[]=0&posted=0&o=1&o_show=4&cmdSearch=++Pesquisar++"
                yield scrapy.Request(next_page, callback=self.parse)


    def parse_contents(self, response):

        data = get_jobDescription(response)
        il = ItemLoader(item=JobVacancyItem(), selector=response)
        il.add_css('job_title', 'h3')
        il.add_css('job_description', 'h4+ p')
        il.add_value('job_description', '\nBenefícios e outras informações:\n'+data['jobBenefits'])
        il.add_value('post_date', data['postDate'])
        il.add_value('scrape_date', date.today().strftime("%d/%m/%Y"))
        il.add_value('job_location', data['jobLocation'])  
        il.add_value('job_category', data['jobCategory'])
        il.add_value('company', data['company'])
        il.add_value('job_href', str(response.url))
        il.add_value('salary', data['salary'])

        yield il.load_item()