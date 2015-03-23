import tornado
from tornado.log import app_log
__author__ = 'robdefeo'
from tornado.web import RequestHandler, asynchronous
from tornado.escape import json_encode
from operator import itemgetter

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

            self.set_status(200)
            self.finish(
                {
                    "res": self.suggest(data["context"])
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

# from suggest.content import Content
# content = Content()


    def suggest(self, context):
        _id_reasons = {}
        for entity in context["entities"]:
            response = self.content.get_reason_list(entity["type"], entity["key"])
            for x in response:
                reason = {
                    "type": entity["type"],
                    "key": entity["key"],
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

        sorted_suggestions = sorted(_id_reasons.values(), key=itemgetter("score"), reverse=True)
        minimum = sorted_suggestions[-1]["score"]
        maximum = sorted_suggestions[0]["score"]
        return list(self.fill(sorted_suggestions[:10], minimum, maximum))


    def fill(self, suggestions_to_fill, minimum, maximum):
        for x in suggestions_to_fill:
            y = self.content.get_product(x["_id"])
            y["s"] = (x["score"] - minimum) / (maximum - minimum)
            yield y
