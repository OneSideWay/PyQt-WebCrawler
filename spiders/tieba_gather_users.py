import threading
import time
from crawler import reset, TaskMutex

class GatherSpider():

    counter = 0

    def __init__(self, status):
        self.status = status
        reset(self.status)
        self.status['running'] = True
        self.file = open(','.join(status['forums']) + '.txt', 'w+')
        self.first_stop_time = time.time()
        self.taskMutex = TaskMutex(self.status)
        threading.Thread(target=self.detect_running).start()
        for i in self.status['forums']:
            self.taskMutex.add_task(url="https://tieba.baidu.com/f?ie=utf-8&kw=" + i, callback=self.parse_main, status=self.status, meta={'tieba': i})
            self.taskMutex.add_task(url="http://tieba.baidu.com/bawu2/platform/listMemberInfo?ie=utf-8&word=" + i, callback=self.parse_member, status=self.status, meta={'tieba': i})

    def detect_running(self):
        self.non_request_threads = threading.active_count()
        while self.counter < self.status['max_get'] and time.time() - self.first_stop_time < 3 and self.status['running']:
            if threading.active_count() > self.non_request_threads:
                self.first_stop_time = time.time()
            self.status['msg'] = '已收集{}条主页URL,请求队列{}个'.format(self.counter, self.taskMutex.task_pool.qsize())
        self.close()

    def parse_main(self, response):
        for i in response.xpath('//li[@data-field]//div[contains(@class, "title")]//@href').extract():
            self.taskMutex.add_task(url=response.urljoin(i), callback=self.parse_inside, status=self.status, meta={'tieba': response.meta['tieba']})
        try:
            next_page = response.xpath(
                '//div[contains(@class, "pagination")]/a[contains(@class, "next")]/@href').extract()[0]
            self.taskMutex.add_task(url=response.urljoin(next_page), callback=self.parse_main, status=self.status, meta={'tieba': response.meta['tieba']})
        except:
            pass

    def parse_inside(self, response):
        for i in response.xpath('//li[contains(@class,"d_name")][@data-field]/a[@data-field]/@href').extract():
            homepage = response.urljoin(i)
            self.counter += 1
            self.file.write(homepage + '\n')
        try:
            next_page = response.xpath(
                '//a[contains(text(), "下一页")]/@href').extract()[0]
            self.taskMutex.add_task(url=response.urljoin(next_page), callback=self.parse_inside, status=self.status, meta={'tieba': response.meta['tieba']})
        except:
            pass

    def parse_member(self, response):
        for member in response.xpath('//span[contains(@class,"member")]'):
            href = member.xpath('div/a/@href').extract()[0]
            homepage = response.urljoin(href)
            self.counter += 1
            self.file.write(homepage + '\n')
        try:
            nextp = response.xpath(
                '//a[@class="next_page"]/@href').extract()[0]
            url = response.urljoin(nextp)
            self.taskMutex.add_task(url=url, callback=self.parse_member, status=self.status, meta={'tieba': response.meta['tieba']})
        except:
            pass

    def close(self):
        self.status['running'] = False
        self.status['msg'] = '已完成收集，共{}个URL'.format(self.counter)
        self.file.close()
        reset(self.status)
