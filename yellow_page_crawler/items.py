
import scrapy
import re
from scrapy.loader.processors import MapCompose, Join


def get_address(add_str):
    address = re.sub(r"-:?|\s+", ' ', ''.join(add_str))
    return ' '.join(address.split())


def get_phone(phone_str):
    phone = str(phone_str)
    phone = re.findall(r'[\+\(]?\+[1-9][0-9 .\-\(\)]{8,}[0-9]', phone)
    return phone


def get_mail(mail_str):
    mail = str(mail_str)
    mail = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", mail)
    return mail


class YellowPageCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    activity = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field(
        input_processor=MapCompose(get_address),
        output_processor=Join(' ')
    )
    mail = scrapy.Field(
        input_processor=MapCompose(get_mail),
        output_processor=Join(' ')
    )
    phone = scrapy.Field(
        input_processor=MapCompose(get_phone),
        output_processor=Join(' ')
    )
