import tornado
from tornado.web import url
from suggest.handlers.root import Root
from suggest import handlers


class Application(tornado.web.Application):
    def __init__(self):
        from suggest.content import Content
        reason_cache = Content()
        from suggest.logic.suggestor import Suggestor

        path_handlers = [
            url(r"/", Root, dict(suggestor=Suggestor(reason_cache)), name="root"),
            url(r"/([0-9a-fA-F]+)/items", handlers.SuggestionItemsHandler, name="suggestion_items"),
            url(r"/cache", handlers.CacheHandler, dict(reason_cache=reason_cache), name="cache"),
            url(r"/status", handlers.StatusHandler, name="status")
        ]

        settings = dict(
            # static_path = os.path.join(os.path.dirname(__file__), "static"),
            # template_path = os.path.join(os.path.dirname(__file__), "templates"),
            debug=tornado.options.options.debug,
        )
        tornado.web.Application.__init__(self, path_handlers, **settings)
