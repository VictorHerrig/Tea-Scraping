import scrapy
from urllib.parse import urljoin
import csv

class TeaSpringSpider(scrapy.Spider):
    name = "teaspring"

    #custom_settings = {
    #
    #}

    start_urls = ['https://www.teaspring.com/green-tea.asp',
                  'https://www.teaspring.com/black-tea.asp',
                  'https://www.teaspring.com/pu-erh-tea.asp',
                  'https://www.teaspring.com/oolong-tea.asp',
                  'https://www.teaspring.com/white-tea.asp',
                  'https://www.teaspring.com/herbal-tea.asp']

    def parse(self, response):
        links = response.xpath('//table[@class="graybox"]//a[not(text())]/@href').extract()
        for l in links:
            url = urljoin(response.url, l)
            yield scrapy.Request(url, callback=self.parse_link)

    def parse_link(self, response):
        url = response.url
        name = response.xpath('//td[@class = "title"]/text()').extract_first()
        category = response.xpath('//td[@class = "sidecart"]//b/text()').extract_first().replace('Chinese ', '') \
            .replace('and Yellow ', '').replace(' Tea', '')
        origin = response.xpath('//td[@class = "text"]//b[text() = "Origin:"]/following-sibling::text()[1]').extract_first()
        harvest = response.xpath('//td[@class = "text"]//b[text() = "Harvest Period:"]/following-sibling::text()[1]').extract_first()
        mainImg = urljoin(url, response.xpath('//img[@name = "mainimg"]/@src').extract_first())
        return {'name': name, 'category': category, 'origin': origin, 'harvest': harvest, 'image_urls': [mainImg]}