from bson import ObjectId
from tornado.log import app_log
from tornado.web import RequestHandler, asynchronous
from tornado.escape import json_encode, url_unescape, json_decode
from suggest.handlers.extractors import ParamExtractor, BodyExtractor
from suggest.data import SuggestionData
from suggest.logic.suggestor import Suggestor


class Root(RequestHandler):
    suggestor = None
    suggestion_data = None
    param_extractor = None
    body_extractor = None

    def initialize(self, suggestor: Suggestor):
        self.suggestor = suggestor
        self.suggestion_data = SuggestionData()
        self.suggestion_data.open_connection()

        self.param_extractor = ParamExtractor(self)
        self.body_extractor = BodyExtractor(self)

    def data_received(self, chunk):
        pass

    def on_finish(self):
        pass

    @asynchronous
    def post(self, *args, **kwargs):
        self.set_header('Content-Type', 'application/json')

        context = self.body_extractor.context()
        suggestion_items = self.suggestor.create_suggestion_items(context)

        # TODO WHAT OF THE CONTEXT DO I STORE HERE? Whole context is a lot context _id could relate to an old

        _id = self.suggestion_data.insert(
            suggestion_items,
            self.param_extractor.locale(),
            context,
            self.param_extractor.user_id(),
            self.param_extractor.application_id(),
            self.param_extractor.session_id()
        )

        self.set_header('Content-Type', 'application/json')
        self.add_header("Location", "/%s" % str(_id))
        self.add_header("_id", str(_id))
        self.set_status(201)
        self.finish()
