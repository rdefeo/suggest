from functools import lru_cache
import tornado
import tornado.escape
from tornado.httpclient import HTTPClient

__author__ = 'robdefeo'


class Content(object):
    @lru_cache(maxsize=16384)
    def get_product(self, _id):
        url = "http://content.jemboo.com/product/%s.json" % _id
        http_client = HTTPClient()
        response = http_client.fetch(url)
        data = tornado.escape.json_decode(response.body)
        return {
            "title": data["title"]
        }

    @lru_cache(maxsize=128)
    def get_reason_list(self, url):
        http_client = HTTPClient()
        response = http_client.fetch(url)
        return tornado.escape.json_decode(response.body)["results"]