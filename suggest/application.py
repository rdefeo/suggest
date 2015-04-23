import tornado
from tornado.web import url
from suggest.handlers.cache import Cache
from suggest.handlers.root import Root
from suggest.handlers.status import Status

__author__ = 'robdefeo'


class Application(tornado.web.Application):
    def __init__(self):
        from suggest.content import Content
        reason_cache = Content()
        from suggest.logic.suggestor import Suggestor
        handlers = [
            url(r"/", Root, dict(suggestor=Suggestor(reason_cache)), name="root"),
            url(r"/cache", Cache, dict(reason_cache=reason_cache), name="cache"),
            url(r"/status", Status, dict(content=Content()), name="status")
        ]

        settings = dict(
            # static_path = os.path.join(os.path.dirname(__file__), "static"),
            # template_path = os.path.join(os.path.dirname(__file__), "templates"),
            debug=tornado.options.options.debug,
        )
        tornado.web.Application.__init__(self, handlers, **settings)
