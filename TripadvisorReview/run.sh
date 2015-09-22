# clean old data first
rm ./output/items.*

START_URL="http://www.tripadvisor.co.uk/Attraction_Review-g274754-d275831-Reviews-Auschwitz_Birkenau_State_Museum-Oswiecim_Lesser_Poland_Province_Southern_Poland.html"
scrapy crawl Tadv -a start_urls=$START_URL -o ./output/items.json -t jsonlines
