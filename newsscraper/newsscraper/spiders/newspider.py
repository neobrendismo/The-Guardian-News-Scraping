import scrapy


class NewspiderSpider(scrapy.Spider):
    name = "newspider"
    allowed_domains = ["www.theguardian.com"]
    start_urls = ["https://www.theguardian.com/au"]

    def parse(self, response):
        pass
