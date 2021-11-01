# Import spiders
from .spiders.bons_empregos import BonsEmpregosSpider
from .spiders.cargadetrabalhos import CargaDeTrabalhosSpider
from .spiders.emprego_org import EmpregoOrgSpider
from .spiders.emprego_xl import EmpregoXlSpider
from .spiders.net_empregos import NetEmpregosSpider

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

# Make sure to be in the Data Collection directory
FOLDER_PATH = "/Users/gilnr/OneDrive - NOVASBE/Work Project/Code/Data/"

def main():
    configure_logging()
    settings = get_project_settings()
    settings.set('FEED_FORMAT', 'jsonlines')
    # settings.set('FEED_URI', 'result.json')
    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks
    def crawl():
        settings.set('FEED_URI', FOLDER_PATH + "BonsEmpregos.json")
        yield runner.crawl(BonsEmpregosSpider)

        settings.set('FEED_URI', FOLDER_PATH + "CargaDeTrabalhos.json")
        yield runner.crawl(CargaDeTrabalhosSpider)

        settings.set('FEED_URI', FOLDER_PATH + "EmpregoOrg.json")
        yield runner.crawl(EmpregoOrgSpider)

        settings.set('FEED_URI', FOLDER_PATH + "EmpregoXl.json")
        yield runner.crawl(EmpregoXlSpider)

        settings.set('FEED_URI', FOLDER_PATH + "NetEmpregos.json")
        yield runner.crawl(NetEmpregosSpider)

        reactor.stop()

    crawl()
    reactor.run() # the script will block here until the last crawl call is finished

if __name__ == '__main__':
    main()