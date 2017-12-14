## Data Extraction and Cleansing using Scrapy - Pycon Pakistan '17

### Introduction
**Data Extraction** is one of the most useful skills in the field of data analytics. It is the first step of a Data Science project and it is followed by **Data Cleansing** process, which fixes inconsistence, incompleteness and incorrectness of data. 

Data can be extracted from a variety of sources such as:
- Databases
- Web Services
- Files - JSON, XML, text etc
- Web Scraping 

In this tutorial we'll be focusing on **Web Scraping** and the tool that we'll be using is Python's [Scrapy](https://docs.scrapy.org/en/latest/). 

### Scrapy 
Scrapy is a web scraping tool with excellent capabilities, some of it's features are as follows: 

- End to end tool for downloading, cleaning and saving data
- Offers adequate post processing
- Can handle websites behind login
- Better error handling and resumable behavior
- Above all, **Asynchronous**

Please follow the [official scrapy documentation](https://doc.scrapy.org/en/latest/index.html) for more information.

### Setting up the environment
You'll need to install Scrapy on your system in order to run this crawler. We recommend you to install scrapy in a separate python virtual environment. You may find the detailed installation guide [here](https://docs.scrapy.org/en/latest/intro/install.html).

### Running the crawler
You can run the crawl using the following command:

`scrapy crawl python_jobs`

If you'd like to save the crawler logs to a log file then you can use the following command:

`scrapy crawl python_jobs --set LOG_FILE=crawler.log`

Finally, if you'd like to store python jobs in JSON format then you can use the `-o` argument:

`scrapy crawl python_jobs -o python-jobs.json`

### How it works
#### The Crawler

Lets discuss how [python_jobs_spider.py](https://github.com/mateen91/scrapy-tutorial/blob/master/stackoverflow_jobs/stackoverflow_jobs/spiders/python_jobs_spider.py) crawls a site. 

```
from scrapy import Request
from scrapy.spiders import CrawlSpider

from stackoverflow_jobs.spiders.utils import clean
```

It starts off by importing scrapy's CrawlSpider and Request classes. We've also imported a clean method from [utils.py](https://github.com/mateen91/scrapy-tutorial/blob/master/stackoverflow_jobs/stackoverflow_jobs/spiders/utils.py) that removes useless space characters from a string or list.

```
class PythonJobsSpider(CrawlSpider):
    name = 'python_jobs'
    start_urls = [
        'https://stackoverflow.com/jobs?sort=i&q=pyhton&l=Berlin%2C+Germany&d=20&u=Km'
    ]
```

Here we've defined a crawler class with its class-level variables. The attribute `name` is the crawler identifier and it's the same name that we used to run the crawl. `start_urls` is a list of URLs that tells the crawler what web pages to request whenever the crawler starts.

```
def parse(self, response):
    job_urls = response.css('.-row .-title .job-link::attr(href)').extract()
    for job_url in job_urls:
        yield Request(url=response.urljoin(job_url), callback=self.parse_job)

    next_page = response.css('.test-pagination-next::attr(href)').extract()
    if next_page:
        yield Request(url=response.urljoin(next_page[0]), callback=self.parse)
```

`parse` is the default method that is called when the response(s) of the URL(s) mentioned in `start_urls` are received. As we need to pick all jobs available in the job listing page, therefore, we've picked the corresponding job page URLs using a CSS selector and requested all of those pages. We've also picked up the URLs for subsequent job listing pages. 

```
def parse_job(self, response):
    item = {}
    item['title'] = self.title(response)
    item['company'] = self.company(response)
    ...
    ...

    yield item
```

You might have noticed that the callback for the job page requests in `parse` was `parse_job`, therefore, we'll be getting response for all job pages in this method. Here we've declared a simple `item` dictionary that will hold data-points regarding a given job. Finally, the method yields the job dictionary. 

Rest of the class methods are just helper methods that take HTTP response as an argument and return corresponding data values.

We've got another implementation of the same crawler i.e. [python_jobs_spider_with_rules.py](https://github.com/mateen91/scrapy-tutorial/blob/master/stackoverflow_jobs/stackoverflow_jobs/spiders/python_jobs_spider_with_rules.py), This crawler uses [CrawlSpider Rules](https://docs.scrapy.org/en/latest/topics/spiders.html#scrapy.spiders.CrawlSpider) which makes crawling  convenient. 

```
rules = (
    Rule(LinkExtractor(restrict_css='.test-pagination-next')),
    Rule(LinkExtractor(restrict_css='.-row .-title .job-link'), callback='parse_job'),
)
```

These rules do exactly the same job as the `parse` method does. We've defined two rules here, first rule requests subsequent listing pages while the second rule requests the job pages and sends their responses to the `parse_job` method 

#### The Pipeline
We've defined a pipeline called `StackoverflowJobsPipeline` in [pipelines.py](https://github.com/mateen91/scrapy-tutorial/blob/master/stackoverflow_jobs/stackoverflow_jobs/pipelines.py).
```
class StackoverflowJobsPipeline(object):
    def process_item(self, item, spider):
        return {k: v for k, v in item.items() if v}
```
After an item gets yielded from the crawler, it's passed to this pipeline. Here we remove the item attributes that are empty and let the rest of the attributes pass through. 

### Credits
- Authors: Ahmed Suffian Javed, Mateen Ahmed
- [Pycon Pakistan '17](pycon.pk)
