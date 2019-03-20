# -*- coding: utf-8 -*-
import scrapy
import time

AGENCIES_PAGES = 4
ROOT_URL = 'https://www.hubspot.com/agencies'
MAIN_URL = 'https://www.hubspot.com'
agencies = []

class Agency ():
    
    def __init__(self,name, website, location, partnership):
        self.name = name
        self.website = website
        self.location = location
        self.partnership = partnership


class HubspotSpider(scrapy.Spider):
    name = 'hubspot'
    
    # Looping over the agencies pages
    def start_requests(self):
        url = ROOT_URL
        
        self.f = open("agencies.txt",mode='a',encoding = 'utf-8')

        print("Parsing agencies page: {}".format(url))
        yield scrapy.Request(url=url, callback=self.parse)
    
 
    def parse_agenicies(self, response):
        # print("Starting with parsing {}".format(response.url.split('/')[4]))

        name = response.css('h2::text').get()
        website = response.css("a.partners-details__hero-website.partners-listing-website::attr('href')").get()
        location = response.css('p.partners-details__hero-location::text').get()
        partnership = response.css('p.partners-details__hero-icon.diamond::text').get()

        # yield {
        #     'name': response.css('h2::text').get(),
        #     'website':response.css("a.partners-details__hero-website.partners-listing-website::attr('href')").get(),
        #     'partner':response.css('p.partners-details__hero-icon.diamond::text').get(),
        #     'location':response.css('p.partners-details__hero-location::text').get(),
        # }       
        agency = Agency(name, website, location, partnership)
        # print("AGENCY: {}".format(agency.name))
        self.f.write("{}, {}, {}, {} \n".format(agency.name, agency.website,agency.location, agency.partnership))
 
    def parse(self, response):

        page_agencies = response.css('a.directories__link::attr("href")').getall()

        for agency in page_agencies:
            agencies.append(MAIN_URL + agency)

        # print("********* There are {} agencies  *********".format(len(agencies)))
        # print(agencies)
        
        # for image in response.css('img::attr(src)'):
        #     yield {
        #         'image': image.get(),
        #     }

        # current_page = response.css('span.page-numbers.current::text').get()

        next_page = response.css("li:nth-child(n+2).directories__page-arrow > a::attr(href)").get()

        print("NEXT PAGE: {}".format(next_page))

        # if (next_page is not None) and (next_page != 'https://www.hubspot.com/agencies?page=4'):
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            print("FINISHED SCRAPING PAGES!")
            for agency in agencies:
                yield scrapy.Request(agency, callback=self.parse_agenicies)
            
            # print("*****************")
            # print("** FINISHED!!! **")
            # print("*****************")

