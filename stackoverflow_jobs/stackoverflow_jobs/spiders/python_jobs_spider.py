import re

from scrapy import Request
from scrapy.spiders import CrawlSpider


class PythonJobsSpider(CrawlSpider):
    name = 'python_jobs'
    start_urls = [
        'https://stackoverflow.com/jobs?sort=i&q=pyhton&l=Berlin%2C+Germany&d=20&u=Km'
    ]

    def parse(self, response):
        job_urls = response.css('.-row .-title .job-link::attr(href)').extract()
        for job_url in job_urls:
            yield Request(url=response.urljoin(job_url), callback=self.parse_job)

        next_page = response.css('.test-pagination-next::attr(href)').extract()
        if next_page:
            yield Request(url=response.urljoin(next_page[0]), callback=self.parse)

    def parse_job(self, response):
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
