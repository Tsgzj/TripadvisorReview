START_URL="http://www.tripadvisor.co.uk/Attraction_Review-g294212-d325811-Reviews-Great_Wall_at_Mutianyu-Beijing.html"

scrapy crawl Tadv -a start_urls=$START_URL -o ./output/items.json
