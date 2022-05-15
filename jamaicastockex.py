# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 04:29:20 2022

@author: RONNY
"""

from scrapy.spiders import Spider
import pandas as pd
from bs4 import BeautifulSoup as BS
import scrapy

class JamaicastockexBot(Spider):
    name='jamaicastockex'
    keyword="sj"
    def start_requests(self):
        url=f'https://www.jamstockex.com/tag/{self.keyword}'
        yield scrapy.Request(url, callback=self.parse)
        
    def parse(self, response):        
        soup=BS(response.text, 'lxml')
        result=[]
        links=soup.select('div.elementor-posts-container:nth-child(2)')
        for i in links:
            url1=i.findAll('a')
            for h in url1:
                url2=h.get('href')
                if url2 not in result:
                    result.append(url2)
                    
        for article in result:
            yield scrapy.Request(url=article, callback=self.parse_article)
                            
    def parse_article(self, response):
        article_db={"Date":[], "Title":[], "Content":[]}
        date=response.css("span.elementor-icon-list-text:nth-child(1)::text").get()
        title=response.css("h1.elementor-heading-title::text").get()
        content=[]
        content.append(response.css("strong::text").getall())
        content.extend(response.css("p::text").getall())
        article_db['Date'].append(date)
        article_db['Title'].append(title)
        article_db['Content'].append(content)
        article_db=pd.DataFrame(article_db)
        article_db.to_csv('E:/clients/alade/jamaicastockex/stockexData/sj.csv',mode='a', index=False, header=False)
        
        
                    
                        
        
        
