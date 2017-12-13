from scrapy.spiders import CrawlSpider


class PythonJobsSpider(CrawlSpider):
    name = 'python_jobs'
    start_urls = [
        'https://stackoverflow.com/jobs/148919/data-scientist-e-commerce-machine-learning-zalando-se',
        'https://stackoverflow.com/jobs/133344/backend-developer-python-python-backend-engineer-celeraone-gmbh'
    ]

    def parse(self, response):
        item = {}
        item['title'] = self.title(response)
        item['company'] = self.company(response)
        item['location'] = self.location(response)
        item['perks'] = self.perks(response)
        item['technologies'] = self.technologies(response)
        item['description'] = self.description(response)
        yield item

    def title(self, response):
        return response.css('.job-detail-header .-title a::text').extract_first()

    def company(self, response):
        return response.css('.job-detail-header .-company .employer::text').extract_first()

    def location(self, response):
        return response.css('.job-detail-header .-company .-location::text').extract_first()

    def perks(self, response):
        return response.css('.job-detail-header .-perks p::text').extract()

    def technologies(self, response):
        return response.css('.-technologies .-tags a::text').extract()

    def description(self, response):
        return response.css('.-about-job-items .-item ::text').extract()
