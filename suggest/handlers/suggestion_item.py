from bson.json_util import dumps
from tornado.web import RequestHandler
from suggest.data import SuggestionData
from suggest.handlers.extractors import PathExtractor, ParamExtractor
from suggest import __version__


class SuggestionItems(RequestHandler):
    suggestion_data = None
    path_extractor = None
    param_extractor = None

    def initialize(self):
        self.suggestion_data = SuggestionData()
        self.suggestion_data.open_connection()

        self.path_extractor = PathExtractor(self)
        self.param_extractor = ParamExtractor(self)

    def data_received(self, chunk):
        pass

    def get(self, suggestion_id, *args, **kwargs):
        suggestion = self.suggestion_data.get(self.path_extractor.suggestion_id(suggestion_id))
        start = self.param_extractor.offset()
        end = start + self.param_extractor.page_size()

        items = suggestion["items"][start:end]

        self.set_status(200)
        self.set_header('Content-Type', 'application/json')
        self.write(
            dumps(
                {
                    "items": items,
                    "version": __version__
                }
            )
        )
        self.finish()

        # TODO 40 write log about what was retrieved

