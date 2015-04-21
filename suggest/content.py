from functools import lru_cache
import tornado
import tornado.escape
from tornado.httpclient import HTTPClient, HTTPError

__author__ = 'robdefeo'


class Content(object):
    @lru_cache(maxsize=128)
    def get_reason_list(self, url):
        try:
            http_client = HTTPClient()
            response = http_client.fetch(url)
            return tornado.escape.json_decode(response.body)["results"]
        except HTTPError as e:
            print("Error=%s,url=%s" % (str(e), url))