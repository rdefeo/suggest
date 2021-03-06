__author__ = 'robdefeo'
from tornado.web import RequestHandler, asynchronous
from tornado.escape import json_encode
from suggest import __version__

class Status(RequestHandler):
    def initialize(self):
        pass

    def on_finish(self):
        pass

    @asynchronous
    def get(self):
        self.set_header('Content-Type', 'application/json')
        self.set_status(200)
        self.finish(
            {
                "status": "OK",
                "version": __version__
                # ,
                # "cache": {
                #     "reason_list": {
                #         "hits": reason_list[0],
                #         "misses": reason_list[1],
                #         "maxsize": reason_list[2],
                #         "currsize": reason_list[3]
                #     }
                # }
            }
        )
