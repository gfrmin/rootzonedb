import scrapy

import datetime

class ZonedbSpider(scrapy.Spider):
    name = 'zonedb'
    allowed_domains = ['iana.org']
    start_urls = ['https://www.iana.org/domains/root/db']

    def parse(self, response):
        domainrows = response.css("#tld-table tr")
        for domainrow in domainrows[1:]:
            domaintds = domainrow.css("td")
            texts = [td.css("::text,a::text").getall()[-1] for td in domaintds]
            domainpage = response.urljoin(domaintds[0].css("a::attr(href)").get())
            textkeys = ['domain', 'type', 'tldmanager']
            item = dict(zip(textkeys, texts))
            item['domainpage'] = domainpage
            item['timestamp'] = datetime.datetime.utcnow().isoformat()
            yield item
