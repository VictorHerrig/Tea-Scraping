import scrapy
from scrapy.crawler import CrawlerProcess
from spiders.TeaSpring import TeaSpringSpider

process = CrawlerProcess({'USER_AGENT': 'TeaScraping (+https://github.com/VictorHerrig)',
                          'ROBOTSTXT_OBEY': True,
                          'ITEM_PIPELINES': {'scrapy.pipelines.images.ImagesPipeline': 1,
                                             'TeaScraping.pipelines.ImageProcessingPipeline': 100,
                                             'TeaScraping.pipelines.WritingPipeline': 1000},
                          'IMAGES_STORE': 'images/',
                          'LOG_ENABLED': False
                          })
process.crawl(TeaSpringSpider)
process.start()