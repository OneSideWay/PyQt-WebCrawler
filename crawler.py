import threading
import string
import queue
import urllib.request
import urllib.parse
import traceback
from parsel import Selector

def reset(status):
    status['counter'] = 0
    status['pct'] = 0

class CustomResponse():

    meta = None
    selector = None
    url = None
    body = None
    status = None
    xpath = None
    css = None

    def __init__(self, url, status, body, meta=None):
        self.url = url
        self.status = status
        self.body = str(body)
        self.meta = meta or {}
        self.selector = Selector(self.body)
        self.xpath = self.selector.xpath
        self.css = self.selector.css

    def urljoin(self, url):
        return urllib.parse.urljoin(self.url, url)

class TaskMutex():

    def __init__(self, status, max_threads=12):
        self.status = status
        self.still_alive = lambda: self.status.get('running')
        self.max_threads = max_threads
        self.task_pool = queue.Queue()
        threading.Thread(target=self.fetch_task).start()

    def add_task(self, **kwargs):
        if self.still_alive():
            self.task_pool.put(kwargs)

    def fetch_task(self):
        while self.still_alive():
            if threading.active_count() <= self.max_threads:
                try:
                    new_request_args = self.task_pool.get(False)
                    RequestThread(**new_request_args).start()
                except:
                    pass

class RequestThread(threading.Thread):

    def __init__(self, url, callback, status, meta=None):
        threading.Thread.__init__(self)
        self.url = url
        self.callback = callback
        self.status = status
        self.meta = meta

    def run(self):
        get = 0
        while get < 3:
            if not self.status.get('running'):
                return
            try:
                res = urllib.request.urlopen(urllib.parse.quote(self.url, safe=string.printable))
                response = CustomResponse(url=self.url, status=res.getcode(), body=res.read())
                res.close()
                response.meta = self.meta
                self.callback(response)
                break
            except Exception as e:
                get += 1
                print(e, 'Request failed for {} times'.format(get))
        self.status['counter'] += 1
