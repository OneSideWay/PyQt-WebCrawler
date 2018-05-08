import threading
from urllib.parse import urlparse, parse_qs
from crawler import TaskMutex, reset

class UserInfoSpider():

    counter = 0
    user_info = {}

    def __init__(self, status):
        self.status = status
        reset(self.status)
        self.status['running'] = True
        self.status.pop('data', None)
        step = 0
        for line in open(self.status['file'], 'r'):
            step += 1
            parsed = urlparse(line[:-1])
            if parsed.scheme and parsed.netloc:
                qs = parse_qs(parsed.query)
                if qs.get('un'):
                    self.user_info[qs['un'][0]] = {}
            self.status['msg'] = '正在分析文件...{}'.format(step)
        self.total = len(self.user_info)
        self.taskMutex = TaskMutex(self.status)
        threading.Thread(target=self.detect_running).start()
        for i in list(self.user_info.keys()):
            self.taskMutex.add_task(url='http://tieba.baidu.com/home/main?ie=utf-8&un=' + i, callback=self.parse, status=self.status, meta={'un': i})

    def detect_running(self):
        self.non_request_threads = threading.active_count()
        while self.status['counter'] < self.total and self.status['running']:
            self.status['msg'] = '已收集 {}/{},请求队列{}个'.format(self.status['counter'], self.total, threading.active_count() - self.non_request_threads)
            self.status['pct'] = self.status['counter'] / self.total * 100
        self.close()

    def parse(self, response):
        self.counter += 1
        if response.xpath('//div[@class="page404"]'):
            return

        item = {}
        forum_name = response.xpath('//script').re(r'"forum_name":"(.*?)"')
        level_id = response.xpath('//script').re(r'"level_id":(.*?),')
        
        forum_name = list(map(lambda x: x.replace('\\\\', '\\').encode('latin-1').decode('unicode_escape'), forum_name))
        item['forums'] = dict(zip(forum_name, level_id))

        outerSel = response.xpath('//span[@class="user_name"]/span')
        sex_sign = response.xpath('//span[contains(@class, "userinfo_sex")]/@class').extract()
        if not sex_sign:
            return
        if 'userinfo_sex_female' in sex_sign[0]:
            item['gender'] = 'female'
        else:
            item['gender'] = 'male'
        #try:
        item['age'] = float(outerSel.xpath('span[2]/text()').extract()[0].split(':')[1].split('\\xe5\\xb9\\xb4')[0])
        #except:
        #    item['age'] = 0.0
        post = outerSel.xpath('span[4]/text()').extract()[0].split(':')[1]
        if '\\xe4\\xb8\\x87' in post or '万' in post:
            item['postNum'] = int(float(post.replace('\\xe4\\xb8\\x87', ''))*10000)
        else:
            item['postNum'] = int(post)
        self.user_info[response.meta['un']] = item

    def close(self):
        self.status['running'] = False
        for i in list(self.user_info.keys()):
            if not self.user_info[i]:
                self.user_info.pop(i, None)
        self.status['msg'] = '已完成收集,共{}条有效用户数据'.format(len(self.user_info))
        self.status['data'] = self.user_info
        reset(self.status)
