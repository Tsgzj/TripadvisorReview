import scrapy

from TripadvisorReview.items import TripadvisorreviewItem

# max number of pages allowed to fetch
# set this to negative or 0 to fetch all
MAX_REVIEWS_PAGES = 10

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def strip_all(mylist):
    result = []
    for i in mylist:
        result.append(strip_tags(i))
    return result


class TadvSpider(scrapy.Spider):
    name = "Tadv"
    base_url = "http://www.tripadvisor.com"
    allowed_domains = ["tripadvisor.com"]
    tripadvisor_items = []
    counter_page_review = 0

    def __init__(self, *args, **kwargs):
      super(TadvSpider, self).__init__(*args, **kwargs)
      self.start_urls = kwargs.get('start_urls').split(',')

    def parse(self, response):
        if (self.counter_page_review < MAX_REVIEWS_PAGES or MAX_REVIEWS_PAGES <
        0):
            self.counter_page_review += 1

            for sel in response.xpath("//div[@id='REVIEWS']"):
                raw_title = sel.xpath("//div[@class='quote isNew']/a/span[@class='noQuotes']").extract()
                raw_entry = sel.xpath("//div[@class='wrap']/div[@class='entry']").extract()
                stripped_title = strip_all(raw_title)
                stripped_entry = strip_all(raw_entry)

                tripadvisor_item = TripadvisorreviewItem()
                tripadvisor_item['title'] = stripped_title
                tripadvisor_item['entry'] = stripped_entry

                self.tripadvisor_items.append(tripadvisor_item)

                next_page_url = strip_tags(sel.xpath("//div[@class='deckTools btm']//a[2]/@href").extract()[0])

                if next_page_url and len(next_page_url) > 0:
                    yield scrapy.Request(self.base_url + next_page_url,
                                     callback=self.parse)
                else:
                    yield self.tripadvisor_items

            else:
                yield self.tripadvisor_items


           # yield scrapy.Request(self.base_url + next_page_url, meta={'tripadvisor_item': tripadvisor_item, 'counter_page_review': 0}, callback=self.parse_follow_next_page)

    # def parse_follow_next_page(self, response):
    #     tripadvisor_item = response.meta['tripadvisor_item']
    #     counter_page_review = response.meta['counter_page_review']
    #     sel = scrapy.Selector(response)

    #     if counter_page_review < MAX_REVIEWS_PAGES:
    #         counter_page_review = counter_page_review + 1

    #         for i in sel.xpath("//div[@id='REVIEWS']"):
    #             raw_title = i.xpath("//div[@class='quote isNew']/a/span[@class='noQuotes']").extract()
    #             raw_entry = i.xpath("//div[@class='wrap']/div[@class='entry']").extract()
    #             stripped_title = strip_all(raw_title)
    #             stripped_entry = strip_all(raw_entry)

    #             tripadvisor_item['title'] = stripped_title
    #             tripadvisor_item['entry'] = stripped_entry

    #         next_page_url = strip_tags(sel.xpath("//div[@class='deckTools btm']//a[2]/@href").extract()[0])

    #         if next_page_url and len(next_page_url) > 0:
    #             yield scrapy.Request(self.base_url + next_page_url,
    #             meta={'tripadvisor_item': tripadvisor_item,
    #                   'counter_page_review': counter_page_review},
    #             callback=self.parse_follow_next_page)
    #         else:
    #             yield tripadvisor_item

    #     else:
    #         yield tripadvisor_item
