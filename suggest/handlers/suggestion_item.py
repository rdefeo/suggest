from bson.json_util import dumps
from tornado.web import RequestHandler, asynchronous

from suggest.data import SuggestionData, SuggestionItemData
from suggest.handlers.extractors import PathExtractor, ParamExtractor
from suggest import __version__


class SuggestionItems(RequestHandler):
    suggestion_data = None
    suggestion_item_data = None
    path_extractor = None
    param_extractor = None

    def initialize(self):
        self.suggestion_data = SuggestionData()
        self.suggestion_data.open_connection()
        self.suggestion_item_data = SuggestionItemData()
        self.suggestion_item_data.open_connection()

        self.path_extractor = PathExtractor(self)
        self.param_extractor = ParamExtractor(self)

    def data_received(self, chunk):
        pass

    @asynchronous
    def get(self, suggestion_id, *args, **kwargs):
        suggestion = self.suggestion_data.get(self.path_extractor.suggestion_id(suggestion_id))
        start = self.param_extractor.offset()
        end = start + self.param_extractor.page_size()

        items = suggestion["items"][start:end]

        self.set_status(200)
        self.set_header('Content-Type', 'application/json')
        self.add_header('next_offset', end)

        self.write(
            dumps(
                {
                    "offset": self.param_extractor.offset(),
                    # "total_items": len(suggestion["items"]),
                    "items": items,
                    "version": __version__
                }
            )
        )
        self.finish()

        self.suggestion_item_data.insert(
            items,
            self.param_extractor.locale(),
            self.param_extractor.application_id(),
            self.param_extractor.session_id(),
            self.param_extractor.offset(),
            self.param_extractor.page_size()
        )
