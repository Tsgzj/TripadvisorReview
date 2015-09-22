import scrapy

from TripadvisorReview.items import TripadvisorreviewItem

# max number of pages allowed to fetch
# set this to negative or 0 to fetch all
MAX_REVIEWS_PAGES = 1000

from HTMLParser import HTMLParser

# Strip html string
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
    tripadvisor_items = TripadvisorreviewItem()
    reviews = []
    counter_page_review = 0

    def __init__(self, *args, **kwargs):
      super(TadvSpider, self).__init__(*args, **kwargs)
      self.start_urls = kwargs.get('start_urls').split(',')

    def parse(self, response):
        for sel in response.xpath("//div[@id='REVIEWS']"):
            # The defulet reviews are shrinked
            # You need to click 'More' to get the complete content
            # To avoid this, click on one of the reviews to jump to
            # expanded reviews

            expanded_review_url = strip_tags(sel.xpath("//div[@class='quote isNew']/a/@href").extract()[0])

            if expanded_review_url and len(expanded_review_url) > 0:
                yield scrapy.Request(self.base_url + expanded_review_url, callback = self.parse_review_page)

    def parse_review_page(self, response):
        if (self.counter_page_review < MAX_REVIEWS_PAGES or MAX_REVIEWS_PAGES <= 0):
            self.counter_page_review += 1

            #for sel in response.xpath("//div[@id='REVIEWS']"):
                # raw_title = sel.xpath("//div[@class='quote isNew']/a/span[@class='noQuotes']").extract()
                # stripped_title = strip_all(raw_title)
                # no need to crawl title
                # tripadvisor_item = TripadvisorreviewItem()
                # tripadvisor_item['title'] = stripped_title
                # tripadvisor_item['entry'] = stripped_entry

            # crappy way
            raw_entry = response.xpath("//div[@class='innerBubble']/div[@class='entry']/p").extract()
            stripped_entry = strip_all(raw_entry)
            self.reviews += stripped_entry

            # check if there is next page
            next_page_url = response.xpath("//div[@class='deckTools btm']//a[contains(@class,'nav next rndBtn rndBtnGreen')]/@href")

            if next_page_url:
                yield scrapy.Request(self.base_url + strip_tags(next_page_url.extract()[0]), callback=self.parse_review_page)
            else:
                self.tripadvisor_items['entry'] = self.reviews
                yield self.tripadvisor_items

        else:
            self.tripadvisor_items['entry'] = self.reviews
            yield self.tripadvisor_items
