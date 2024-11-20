import scrapy


class LightingSpider(scrapy.Spider):
    name = "lighting"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/lighting"]

    def parse(self, response):
        products = response.xpath("//div[contains(@class, 'product-item')]")
        for product in products:
            name = product.xpath(".//a[contains(@class, 'product-item__name')]/text()").get()
            price = product.xpath(".//span[contains(@class, 'product-item__price')]/text()").get()
            link = product.xpath(".//a[contains(@class, 'product-item__name')]/@href").get()
            if link and not link.startswith("http"):
                link = response.urljoin(link)

            yield {
                "name": name.strip() if name else None,
                "price": price.strip() if price else None,
                "link": link,
            }

        next_page = response.xpath("//a[contains(@class, 'pagination-next')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
