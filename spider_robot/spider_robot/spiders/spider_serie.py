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
        links = response.css("div.tec--list--lg").css(".tec--list__item").css("h3").css("a::attr(href)").getall()
        for link in links:
            yield scrapy.Request(link, callback=self.noticia)
        pass
        next_page = response.css('a.tec--btn::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
    
    def noticia(self, response):
        content = ""
        for line in response.css(".tec--article__body-grid").getall():
            content = content + "".join(line) + "\n"

            # Pega somente o primeiro parágrfo da noticia, por questão de performance, para não ter um texto mto grande
            contentBody = response.css("div.tec--article__body").css("p::text").get()

            #print(content)
            post = {
                'title': response.css("h1.tec--article__header__title::text").get(),
                'date': response.css("div.tec--timestamp__item").css("strong::text").get(),
                'author': response.css("div.tec--timestamp__item").css("a::text").get(),
                'text': contentBody,
                #'content': content.encode('utf-8')
            }
            print(post)
            yield post
 