from bson import ObjectId
from tornado.log import app_log
from tornado.web import RequestHandler, asynchronous
from tornado.escape import json_encode, url_unescape, json_decode


class Root(RequestHandler):
    def initialize(self, suggestor):
        self.suggestor = suggestor

    def on_finish(self):
        pass

    @asynchronous
    def get(self, *args, **kwargs):
        self.set_header('Content-Type', 'application/json')
        session_id = self.get_argument("session_id", None)
        user_id = self.get_argument("user_id", None)
        application_id = self.get_argument("application_id", None)
        locale = self.get_argument("locale", None)
        raw_offset = self.get_argument("offset", None)
        raw_page_size = self.get_argument("page_size", None)
        raw_context = self.get_argument("context", None)

        if application_id is None:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "missing param=application_id"
                    }
                )
            )
        elif session_id is None:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "missing param=session_id"
                    }
                )
            )
        elif raw_offset is None:
            self.set_status(412)
            self.finish(
                {
                    "status": "error",
                    "message": "missing param=offset"
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
            offset = int(raw_offset)
            page_size = int(raw_page_size)
            context = json_decode(url_unescape(raw_context))
            suggestion_response, minimum, maximum_score = self.suggestor.score_suggestions(context, offset, page_size)


            self.set_status(200)
            self.finish(suggestion_response)

            if self.get_argument("skip_mongodb_log", None) is None:
                # log_offset = 0
                # log_page_size = 10

                from suggest.data.suggestion import Suggestion
                suggestion_data = Suggestion()
                suggestion_data.open_connection()
                suggestion_data.insert(
                    suggestion_response["suggestions"],
                    locale,
                    ObjectId(context["_id"]),
                    ObjectId(user_id) if user_id is not None else None,
                    ObjectId(application_id),
                    ObjectId(session_id),
                    offset,
                    page_size,
                    maximum_score
                )
                suggestion_data.close_connection()