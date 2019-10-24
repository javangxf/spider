# -*- coding: utf-8 -*-
import time

import scrapy

from spider.items import *


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com']

    '''对主页进行解析'''

    def parse(self, response):
        # 解析出每个电影名，形成列表
        movies = response.xpath("//li[@data-title]")
        for movie in movies:
            try:
                detail_url = response.xpath("//li[@class='poster']/a/@href").extract()
                # print(detail_url)
                yield scrapy.Request(url=detail_url[0], callback=self.film_parse)
            except IndexError as e:
                print(e)

    '''获取电影的详情页'''

    def film_parse(self, response):
        item = MoviesItem()
        dname = ""
        info = response.xpath('//*[@id="content"]')
        name = response.xpath('//h1/span[1]').extract()

        rate = info.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong').extract()[0]
        directors = info.xpath('//*[@id="info"]/span[1]/span[2]/a')
        for director in directors:
            dname += director.xpath('./text()').extract()[0] + "/"
        url = response.xpath('//*[@id="info"]/span[1]/span[2]/a/@href').extract()
        for i in url:
            # print(i)
            yield scrapy.Request(url="https://movie.douban.com" + i, callback=self.director_parse)
        item['name'] = name
        item['rate'] = rate
        item['director'] = dname[0:-1]

        yield item

    '''对导演页面进行解析'''

    def director_parse(self, response):
        item = DirectorItem()
        info = response.xpath('//*[@id="content"]')
        name = info.xpath('./h1').extract()
        gender = info.xpath('//div[@class="info"]/ul/li[1]').extract()
        constellation = info.xpath('//div[@class="info"]/ul/li[2]').extract()
        films = response.xpath('//*[@id="recent_movies"]/div[2]/ul[1]/li/div[1]/a')
        fname = ""
        for film in films:
            url = film.xpath('./@href').extract()[0]
            # print(film.xpath('./@title').extract())
            fname += film.xpath('./img/@alt').extract()[0] + "/"
            time.sleep(1000)
            yield scrapy.Request(url=url, callback=self.film_parse)
        item['name'] = name
        item['gender'] = gender
        item['constellation'] = constellation
        item['films'] = fname
        yield item
