import scrapy

from TripadvisorReview.items import TripadvisorreviewItem

class TadvSpider(scrapy.Spider):
    name = "Tadv"
    allowed_domains = ["tripadvisor.com"]
    start_urls = [
  "http://www.tripadvisor.co.uk/Attraction_Review-g294212-d311534-Reviews-Temple_of_Heaven_Tiantan_Park-Beijing.html"   ]

    def parse(self, response):
        for sel in response.xpath("//div[@id='REVIEWS']"):
            item = TripadvisorreviewItem()
            item['title'] = sel.xpath("//span[@class='noQuotes']").extract()
            item['entry'] = sel.xpath("//div[@class='entry']").extract()

            yield item
