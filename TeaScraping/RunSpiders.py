import scrapy
from scrapy.crawler import CrawlerProcess
#from spiders.TeaSpring import TeaSpringSpider
#from spiders.AshaTeaHouse import AshaSpider
#from spiders.EsGreen import EsGreenSpider
from spiders import TeaSpiders

process = CrawlerProcess({'USER_AGENT': 'TeaScraping (+https://github.com/VictorHerrig)',
                          'ROBOTSTXT_OBEY': True,
                          'ITEM_PIPELINES': {'scrapy.pipelines.images.ImagesPipeline': 1,
                                             'TeaScraping.pipelines.ImageProcessingPipeline': 100,
                                             'TeaScraping.pipelines.WritingPipeline': 1000},
                          'IMAGES_STORE': 'images/',
                          'LOG_ENABLED': False
                          })
process.crawl(TeaSpiders.TeaSpringSpider)
process.crawl(TeaSpiders.AshaSpider)
process.crawl(TeaSpiders.EsGreenSpider)
process.crawl(TeaSpiders.MeiLeafSpider)
process.crawl(TeaSpiders.IppodoSpider)
process.start()
process.stop()