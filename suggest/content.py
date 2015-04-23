from pylru import FunctionCacheManager
import tornado
import tornado.escape
from tornado.httpclient import HTTPClient, HTTPError

__author__ = 'robdefeo'


class Content(object):
    def __init__(self, cache_maxsize=128):
        self.reason_cache = FunctionCacheManager(self.get_reason_list, cache_maxsize)

    def clear(self):
        self.reason_cache.clear()

    def get_reason_list(self, url):
        try:
            http_client = HTTPClient()
            response = http_client.fetch(url)
            return tornado.escape.json_decode(response.body)["results"]
        except HTTPError as e:
            print("Error=%s,url=%s" % (str(e), url))