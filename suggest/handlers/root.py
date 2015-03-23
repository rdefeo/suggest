import tornado
from tornado.log import app_log
__author__ = 'robdefeo'
from tornado.web import RequestHandler, asynchronous
from tornado.escape import json_encode
from operator import itemgetter
from suggest.settings import CONTEXT_URL


class Root(RequestHandler):
    def initialize(self, content):
        self.content = content

    def on_finish(self):
        pass

    @asynchronous
    def post(self, *args, **kwargs):
        try:
            data = tornado.escape.json_decode(self.request.body)

            if "locale" not in data:
                self.set_status(412)
                self.finish(
                    json_encode(
                        {
                            "status": "error",
                            "message": "missing param=locale"
                        }
                    )
                )

            if "context" not in data:
                self.set_status(412)
                self.finish(
                    json_encode(
                        {
                            "status": "error",
                            "message": "missing param=context"
                        }
                    )
                )

            page = data["page"] if "page" in data else 1
            page_size = data["page_size"] if "page_size" in data else 10
            suggestions = self.suggest(data["context"], page, page_size)

            self.set_header('Content-Type', 'application/json')
            self.set_status(200)
            self.finish(
                {
                    "suggestions": suggestions,
                    "version": "0.0.1"
                }
            )

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

    def suggest(self, context, page, page_size):
        _id_reasons = {}
        self.process_response(
            self.content.get_reason_list(
                "%s/popular.json" % CONTEXT_URL
            ),
            "popular", "popular", "inferred", _id_reasons
        )
        for entity in context["entities"]:
            response = self.content.get_reason_list(
                "%s%s/%s.json" % (CONTEXT_URL, entity["type"], entity["key"])
            )
            self.process_response(response, entity["type"], entity["key"], "detection", _id_reasons)

        sorted_suggestions = sorted(_id_reasons.values(), key=itemgetter("score"), reverse=True)
        minimum = sorted_suggestions[-1]["score"]
        maximum = sorted_suggestions[0]["score"]
        start = (page-1) * page_size
        end = page * page_size
        return list(self.fill(sorted_suggestions[start:end], minimum, maximum))

    def process_response(self, response, _type, key, source, _id_reasons):
        for x in response:
            reason = {
                "source": source,
                "type": _type,
                "key": key,
                "score": x["score"]
            }
            if x["_id"] in _id_reasons:
                _id_reasons[x["_id"]]["reasons"].append(reason)
                _id_reasons[x["_id"]]["score"] += reason["score"]
            else:
                _id_reasons[x["_id"]] = {
                    "reasons": [reason],
                    "score": reason["score"],
                    "_id": x["_id"]
                }

    def fill(self, suggestions_to_fill, minimum, maximum):
        for x in suggestions_to_fill:
            y = self.content.get_product(x["_id"])
            y["s"] = (x["score"] - minimum) / (maximum - minimum)
            y["_id"] = x["_id"]
            yield y
