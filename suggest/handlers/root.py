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

        # elif raw_offset is None:
        #     self.set_status(412)
        #     self.finish(
        #         {
        #             "status": "error",
        #             "message": "missing param=offset"
        #         }
        #     )
        #
        # elif raw_page_size is None:
        #     self.set_status(412)
        #     self.finish(
        #         {
        #             "status": "error",
        #             "message": "missing param=page_size"
        #         }
        #     )
        #
        # elif locale is None:
        #     self.set_status(412)
        #     self.finish(
        #         {
        #             "status": "error",
        #             "message": "missing param=locale"
        #         }
        #     )
        #
        # elif raw_context is None:
        #     self.set_status(412)
        #     self.finish(
        #         {
        #             "status": "error",
        #             "message": "missing param=context"
        #         }
        #     )
        # else:
        #     offset = int(raw_offset)
        #     page_size = int(raw_page_size)
        #     context = json_decode(url_unescape(raw_context))
        #     suggestion_response = self.suggestor.get_suggestion_response(context, offset, page_size)
        #
        #     self.set_status(200)
        #     self.finish(suggestion_response)
        #
        #     if self.get_argument("skip_mongodb_log", None) is None:
        #         from suggest.data.suggestion import Suggestion
        #         suggestion_data = Suggestion()
        #         suggestion_data.open_connection()
        #         suggestion_data.insert(
        #             suggestion_response["suggestions"],
        #             locale,
        #             ObjectId(context["_id"]),
        #             ObjectId(user_id) if user_id is not None else None,
        #             ObjectId(application_id),
        #             ObjectId(session_id),
        #             offset,
        #             page_size
        #         )
        #         suggestion_data.close_connection()