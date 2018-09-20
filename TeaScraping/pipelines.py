# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from urllib.parse import urljoin
import json
from PIL import Image
#import numpy as np
import os
            #item['image_pixels'] = {'array': imgArr.tolist(), 'shape': imgArr.shape}

OUT_PATH = 'out/'

#Processes the request from teaspring
class TeaspringProcessingPipeline(object):
    def process_item(self, item, spider):
        response = item['response']
        url = str(item['url'])
        name = response.xpath('//td[@class = "title"]/text()').extract_first()
        category = response.xpath('//td[@class = "sidecart"]//b/text()').extract_first().replace('Chinese ', '') \
            .replace('and Yellow ', '').replace(' Tea', '')
        origin = response.xpath('//td[@class = "text"]//b[text() = "Origin:"]/following-sibling::text()[1]').extract_first()
        harvest = response.xpath('//td[@class = "text"]//b[text() = "Harvest Period:"]/following-sibling::text()[1]').extract_first()
        mainImg = urljoin(url, response.xpath('//img[@name = "mainimg"]/@src').extract_first() )
        return {'name' : name, 'category' : category, 'origin' : origin, 'harvest' : harvest, 'image_urls' : [mainImg]}

class ImageProcessingPipeline(object):
    def process_item(self, item, spider):
        paths = [img['path'] for img in item['images']]
        if paths:
            item['alt_img_paths'] = []
            #item['image_pixels'] = []
        for path in paths:
            imgPath = 'images/' + path
            image = Image.open(imgPath)
            size = image.size
            #Crop the image to a box if not already
            if (size[0] - size[1]) > 1:
                image = image.crop(((size[0] - size[1]) / 2,size[0] - ((size[0] - size[1]) / 2),0,size[1]))
            elif (size[1] - size[0]) > 1:
                image = image.crop((0, size[0], (size[1] - size[0]) / 2, size[1] - ((size[1] - size[0]) / 2)))
            image = image.resize((512, 512))
            #imgArr = np.array(image)
            altPath = imgPath.replace("full", "alt")
            if not os.path.exists(os.path.dirname(altPath)):
                os.makedirs(os.path.dirname(altPath))
            image.save(altPath)
            item['alt_img_paths'].append(altPath)
        return item


class WritingPipeline(object):
    def open_spider(self, spider):
        if not os.path.exists(os.path.dirname(OUT_PATH)):
            os.makedirs(os.path.dirname(OUT_PATH))
        self.file = open(OUT_PATH + spider.name + '_results.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item