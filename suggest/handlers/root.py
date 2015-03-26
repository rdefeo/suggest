from tornado.log import app_log
from tornado.web import RequestHandler, asynchronous
from tornado.escape import json_encode, url_unescape, json_decode
from operator import itemgetter
from suggest.settings import CONTEXT_URL
from collections import defaultdict


class Root(RequestHandler):
    def initialize(self, suggestor):
        self.suggestor = suggestor

    def on_finish(self):
        pass

    @asynchronous
    def get(self, *args, **kwargs):
        self.set_header('Content-Type', 'application/json')

        locale = self.get_argument("locale", None)
        raw_page = self.get_argument("page", None)
        raw_page_size = self.get_argument("page_size", None)
        raw_context = self.get_argument("context", None)

        if raw_page is None:
            self.set_status(412)
            self.finish(
                {
                    "status": "error",
                    "message": "missing param=page"
                }
            )

        elif raw_page_size is None:
            self.set_status(412)
            self.finish(
                {
                    "status": "error",
                    "message": "missing param=page_size"
                }
            )

        elif locale is None:
            self.set_status(412)
            self.finish(
                {
                    "status": "error",
                    "message": "missing param=locale"
                }
            )

        elif raw_context is None:
            self.set_status(412)
            self.finish(
                {
                    "status": "error",
                    "message": "missing param=context"
                }
            )
        else:
            page = int(raw_page)
            page_size = int(raw_page_size)
            context = json_decode(url_unescape(raw_context))
            suggestion_response = self.suggestor.score_suggestions(context, page, page_size)

            self.set_status(200)
            self.finish(suggestion_response)

            # TODO Log stuff here



