from app import models
import scrapy
import IPython
from app import db
from datetime import datetime

class BedpageSpider(scrapy.Spider):
    name = "all_places_spider"
    start_urls = ["https://www.bedpage.com"]

    def parse(self, response):
        for subsite in response.xpath("//a/@href"):
            url = subsite.root
            if "backpage" in url:
                place = models.Places(url)
                db.session.add(place)
                db.session.commit()


class ScrapePlace(scrapy.Spider):
    name = "specific_place_spider"
    start_urls = [elem.place + "WomenSeekMen/"
                  for elem in models.Places.query.all()]

    def parse(self, response):
        for ad in response.xpath("//a/@href"):
            ending = ad.split("/")[-1]
            try:
                ad_id = int(ending)
                ad = AdUrls(ad, False)
                db.session.add(ad)
                db.session.commit()
            except:
                continue

            
def is_phone_number(elem):
    if len(elem) == 10 or len(elem) == 11:
        try:
            int(elem)
            return True
        except:
            return False
    else:
        return False

    
def parse_string_for_phone_number(content):
    words = content.split()
    for word in words:
        if is_phone_number(word):
            return word
    return ''


class AdBodySpider(scrapy.Spider):
    name = "ad_body_spider"
    start_urls = [elem.url for elem in AdUrls.query.all() if not elem.scraped]

    def parse(self, response):
        title = response.xpath('//div[@id="postingTitle"]//h1').text_content()
        date_posted = response.xpath('//div[@class="adInfo"]').text_content()
        date_posted = date_posted.split("Posted:")[1].strip()
        url = response.root
        body = response.xpath('//div[@class="postingBody"]').text_content()
        phone_number_body = parse_string_for_phone_number(body)
        phone_number_title = parse_string_for_phone_number(title)
        ad_obj = AdInfo(
            title,
            body
            phone_number,
            date_posted,
            url,
            phone_number_body,
            phone_number_title
        )
        db.session.add(ad_obj)
        db.session.commit()
