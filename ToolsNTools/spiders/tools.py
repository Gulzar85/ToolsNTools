import scrapy
import scraper_helper as sh


class ToolsSpider(scrapy.Spider):
    name = 'tools'
    start_urls = ['https://www.toolsntoolsuk.co.uk/']

    def parse(self, response):
        links = response.css('.hover-mask a:nth-child(1)::attr(href)').getall()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_category)
    
    def parse_category(self, response):
        links = response.css('.hover-mask a:nth-child(1)::attr(href)').getall()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_products, dont_filter=True)

    def parse_products(self, response):
        links = response.css('.product-title a::attr(href)').getall()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_product, dont_filter=True)
    
    def parse_product(self, response):
        yield {
            'Product_Name': sh.cleanup(response.css('.product_title.entry-title::text').get()),
            'Product_Price': float(response.css('.basel-scroll-content ins bdi::text').get()),
            'Availability': response.css('p:contains("stock")::text').get(),
            'SKU': response.css('.sku::text').get(),
            'Category': response.css('.posted_in a::text').get(),
            'URL': response.url,
            'image_urls': [response.css('.woocommerce-product-gallery__image a::attr(href)').get()],
            }