# clean old data first
rm ./output/items.*

START_URL="http://www.tripadvisor.com/Attraction_Review-g294212-d311538-Reviews-Summer_Palace_Yiheyuan-Beijing.html"
scrapy crawl Tadv -a start_urls=$START_URL -o ./output/items.jsonl -t jsonlines
