import tornado
from tornado.httpclient import HTTPClient, AsyncHTTPClient
from tornado.log import app_log
from suggest import content

__author__ = 'robdefeo'
from tornado.web import RequestHandler, asynchronous
from tornado.escape import json_encode

class Root(RequestHandler):
    def initialize(self):
        pass

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

            _id_reasons = {}
            for entity in data["context"]["entities"]:
                response = content.get_reason_list(entity["type"], entity["key"])

                for x in response:
                    reason = self.create_reason(entity["type"], entity["key"], x["score"])
                    if x["_id"] in _id_reasons:
                        self.update_suggestion(_id_reasons[x["_id"]], reason)
                    else:
                        _id_reasons[x["_id"]] = self.create_suggestion(x["_id"], reason)

            from operator import itemgetter
            sorted_suggestions = sorted(_id_reasons.values(), key=itemgetter("score"), reverse=True)
            fill_suggestions = []
            for x in sorted_suggestions[:10]:

                x.update(content.get_product(x["_id"]))
                fill_suggestions.append(x)

            self.set_status(200)
            self.finish({
                "res": fill_suggestions
            })

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

    def update_suggestion(self, suggestion, reason):
        suggestion["reasons"].append(reason)
        suggestion["score"] += reason["score"]

    def create_suggestion(self, _id, reason):
        return {
            "reasons": [reason],
            "score": reason["score"],
            "_id": _id
        }
    def create_reason(self, _type, key, score):
        return {
            "type": _type,
            "key": key,
            "score": score
        }

