from tornado import gen
import tornado
from tornado.httpclient import AsyncHTTPClient
from tornado.web import RequestHandler, asynchronous
from tornado.escape import json_encode


class Cache(RequestHandler):
    def initialize(self, reason_cache):
        self.reason_cache = reason_cache

    def on_finish(self):
        pass

    def delete(self, *args, **kwargs):
        self.reason_cache.clear()