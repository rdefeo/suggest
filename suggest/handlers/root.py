from tornado.log import app_log

__author__ = 'robdefeo'
from tornado.web import RequestHandler, asynchronous
from tornado.escape import json_encode

class Root(RequestHandler):
    def initialize(self):
        pass

    def on_finish(self):
        pass

    @asynchronous
    def post(self, *args, **kwargs):
        try:
            raise Exception()
        except Exception as e:
            app_log.error("error=%s" % e)
            self.set_status(500)
            self.finish(
                json_encode(
                    {
                        "status": "error"
                    }
                )
            )
