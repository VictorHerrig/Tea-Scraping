import scrapy
from urllib.parse import urljoin
import re

NAME_NORMALIZATION = False
YELLOW_IS_WHITE = True

class TeaSpringSpider(scrapy.Spider):
    name = "teaspring"

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

class AshaSpider(scrapy.Spider):
    name = "asha"
    start_urls = ['https://www.ashateahouse.com/collections/black',
                  'https://www.ashateahouse.com/collections/dark-oolong',
                  'https://www.ashateahouse.com/collections/green',
                  'https://www.ashateahouse.com/collections/light-oolong',
                  'https://www.ashateahouse.com/collections/puer',
                  'https://www.ashateahouse.com/collections/select-grade',
                  'https://www.ashateahouse.com/collections/white-tea']

    def parse(self, response):
        links = response.xpath('//div[@class="product-grid clearfix"]//a/@href').extract()
        for l in links:
            url = urljoin(response.url, l)
            yield scrapy.Request(url, callback=self.parse_link)

    def parse_link(self, response):
        category = response.xpath('//ul[@class="breadcrumbs colored-links"]/li[3]/a/text()').extract_first()
        name = response.xpath('//ul[@class="breadcrumbs colored-links"]/li[4]/text()').extract_first()
        if NAME_NORMALIZATION:
            name = re.sub('(\(|\[).*(\)|\])', '', name)
        origin = response.xpath('//h2[@class="vendor"]/a/text()').extract_first()
        mainImg = response.xpath('//article/div/div/a/@href').extract_first()
        mainImg = 'https:' + re.sub('\?v=.*', '', mainImg)
        return {'name': name, 'category': category, 'origin': origin, 'image_urls': [mainImg]}

class EsGreenSpider(scrapy.Spider):
    name = "esgreen"
    start_urls = ['https://www.esgreen.com/tea/white-tea',
                  'https://www.esgreen.com/tea/green-tea',
                  'https://www.esgreen.com/tea/yellow-tea',
                  'https://www.esgreen.com/tea/oolong-tea',
                  'https://www.esgreen.com/tea/black-tea']

    def parse(self, response):
        links = response.xpath('//h2[@class="product-name"]/a/@href').extract()
        for l in links:
            url = urljoin(response.url, l)
            yield scrapy.Request(url, callback=self.parse_link)

    def parse_link(self, response):
        category = response.xpath('//div[@class="product-category-title"]/text()').extract_first()
        if category == 'Default Category':
            category = 'NA'
        name = response.xpath('//div[@class="product-name"]/h1/text()').extract_first()
        if NAME_NORMALIZATION:
            name = re.sub('[\-]*[\(\[].*[\)\]]', '', name)
            name = re.sub('[\-]*#[0-9]*', '', name)
        origin = response.xpath('//table[@id="product-attribute-specs-table"]/tbody/tr[7]/td/text()').extract_first()
        origin = (origin.split(',')[-2] + ',' + origin.split(',')[-1]).replace('.', '')
        if ' of ' in origin:
            origin = (origin.split(',')[1]).replace(' of ', ',')
        moreImgs = response.xpath('//ul[@id="shopper_gallery_carousel"]/li//a/@href').extract()
        return {'name': name, 'category': category, 'origin': origin, 'image_urls': moreImgs}

class MeiLeafSpider(scrapy.Spider):
    name = 'meileaf'
    start_urls = ['https://meileaf.com/teas/pure/']

    def parse(self, response):
        links = response.xpath('//h2[@class="product-card__title"]/a/@href').extract()
        for l in links:
            url = urljoin(response.url, l)
            yield scrapy.Request(url, callback=self.parse_link)

    def parse_link(self, response):
        category = response.xpath('//div[contains(@class,"page-heading")]/div/ol/li[2]/a/span/text()').extract_first()
        category = 'Ripe Pu\'er' if category == 'Ripened' else category
        category = 'White' if category == 'Yellow' and YELLOW_IS_WHITE else category
        name = response.xpath('//h1[contains(@class,"product-info__title")]/text()').extract_first()
        origin = response.xpath('//dd[meta/@content="Origin"]/span/text()').extract_first()
        if not origin:
            origin = 'NA'
        origin = origin.replace('\n', '').replace(' ', '')
        imgs = response.xpath('//div[contains(@class, "image-gallery")]/img/@src').extract()
        fullImgs = []
        for img in imgs:
            if 'meileaf.com' in img:
                fullImgs.append(img)
            else:
                fullImgs.append('https://meileaf.com' + img)
        return {'name': name, 'category': category, 'origin': origin, 'image_urls': fullImgs}

class IppodoSpider(scrapy.Spider):
    name = 'ippodo'
    start_urls = ['http://shop.ippodo-tea.co.jp/kyoto/shopf/goods/matcha.html',
                  'http://shop.ippodo-tea.co.jp/kyoto/shopf/goods/gyokuro.html',
                  'http://shop.ippodo-tea.co.jp/kyoto/shopf/goods/sencha.html',
                  'http://shop.ippodo-tea.co.jp/kyoto/shopf/goods/bancha.html']

    def parse(self, response):
        links = response.xpath('//div[contains(@class, "item_list")]/ul/li/div[contains(@class, "item_type")][1]/h5[1]/a/@href').extract()
        for l in links:
            url = urljoin(response.url, l)
            yield scrapy.Request(url, callback=self.parse_link)

    def parse_link(self, response):
        category = response.xpath('//input[contains(@name,"indexForm:cid")]//@value').extract_first()
        name = response.xpath('//span[contains(@id,"goodsDetailsNote1PC")]/text()').extract_first()
        origin = 'Japan'
        imgs = response.xpath('//ul[contains(@class, "thumbs")]/li/a/img/@src').extract()
        imgURLs = []
        for img in imgs:
            imgURLs.append(urljoin(response.url, img))
        return {'name': name, 'category': category, 'origin': origin, 'image_urls': imgURLs}