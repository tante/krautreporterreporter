from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from krautreporterreporter.items import KrautreporterFunding

class Krautreporterspider(CrawlSpider):
    name = "Krautreporterspider"
    allowed_domains = ["krautreporter.de"]
    start_urls = ["https://krautreporter.de/projects/1-das-magazin/backings"]
    rules = (
            #extract only links to other backer pages
            Rule(SgmlLinkExtractor(allow="backings\?page"), callback="parse_item", follow=True),
    )

    def parse_item(self,response):
        select = Selector(response)
        l = select.xpath('//div[@class="user--block"]')
        fundings = []
        for entry in l:
            name = entry.xpath("p/text()")[0].extract()
            amount = entry.xpath("p/text()")[1].extract()[1:]
            funding = KrautreporterFunding()
            if name!="\n":
                funding['name']= name
                funding['amount'] = amount
                fundings.append(funding)
        return fundings
        
            

