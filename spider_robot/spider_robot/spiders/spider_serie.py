import scrapy
import os
import pathlib
import csv
import json
import requests

class SpiderSerieSpider(scrapy.Spider):
    name = 'spider_serie'
    allowed_domains = ['www.tecmundo.com.br']
    start_urls = ['https://www.tecmundo.com.br/minha-serie/']

    def parse(self, response):
        links = response.css("div.tec--list").css(".tec--list__item").css("h3").css("a::attr(href)").getall()
        for link in links:
            yield scrapy.Request(link, callback=self.noticia)
        pass
    
    def noticia(self, response):
        content = ""
        for line in response.css(".tec--article__body-grid").getall():
            content = content + "".join(line) + "\n"
            contentBody = response.css("div.tec--article__body").css("p::text").get().encode('utf-8')

            #print(content)
            post = {
                'title': response.css("h1.tec--article__header__title::text").get().encode('utf-8'),
                'date': response.css("div.tec--timestamp__item").css("strong::text").get(),
                'author': response.css("div.tec--timestamp__item").css("a::text").get().encode('utf-8'),
                'text': contentBody,
                #'content': content.encode('utf-8')
            }
            print(post)
            yield post
 