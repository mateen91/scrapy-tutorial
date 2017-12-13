import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class PythonJobsWithRulesSpider(CrawlSpider):
    name = 'python_jobs_with_rules'
    start_urls = [
        'https://stackoverflow.com/jobs?sort=i&q=pyhton&l=Berlin%2C+Germany&d=20&u=Km'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css='.test-pagination-next')),
        Rule(LinkExtractor(restrict_css='.-row .-title .job-link'), callback='parse_job'),
    )

    def parse_job(self, response):
        item = {}
        item['title'] = self.title(response)
        item['company'] = self.company(response)
        item['location'] = self.location(response)
        item['perks'] = self.perks(response)
        item['technologies'] = self.technologies(response)
        item['description'] = self.description(response)
        item['url'] = response.url
        yield item

    def title(self, response):
        return response.css('.job-detail-header .-title a::text').extract_first()

    def company(self, response):
        return response.css('.job-detail-header .-company .employer::text').extract_first()

    def location(self, response):
        return self.clean(response.css('.job-detail-header .-company .-location::text').extract_first())

    def perks(self, response):
        return self.clean(response.css('.job-detail-header .-perks p::text').extract())

    def technologies(self, response):
        return response.css('.-technologies .-tags a::text').extract()

    def description(self, response):
        return self.clean(response.css('.-about-job-items .-item ::text').extract())

    def clean(self, to_clean):
        if isinstance(to_clean, str):
            return re.sub('\s+', ' ', to_clean).strip()
        return [re.sub('\s+', ' ', d).strip() for d in to_clean if d.strip()]
