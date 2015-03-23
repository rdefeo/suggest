__author__ = 'robdefeo'
from tornado.web import RequestHandler, asynchronous
from tornado.escape import json_encode

class Status(RequestHandler):
    def initialize(self, content):
        self.content = content

    def on_finish(self):
        pass

    @asynchronous
    def get(self):
        detail = self.content.get_product.cache_info()
        reason_list = self.content.get_reason_list.cache_info()
        self.set_header('Content-Type', 'application/json')
        self.set_status(200)
        self.finish(
            {
                "status": "OK",
                "cache": {
                    "detail": {
                        "hits": detail[0],
                        "misses": detail[1],
                        "maxsize": detail[2],
                        "currsize": detail[3]
                    },
                    "reason_list": {
                        "hits": reason_list[0],
                        "misses": reason_list[1],
                        "maxsize": reason_list[2],
                        "currsize": reason_list[3]
                    }
                }
            }
        )
