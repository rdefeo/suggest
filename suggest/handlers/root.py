from tornado.log import app_log
from tornado.web import RequestHandler, asynchronous
from tornado.escape import json_encode, url_unescape, json_decode
from operator import itemgetter
from suggest.settings import CONTEXT_URL
from collections import defaultdict


class Root(RequestHandler):
    def initialize(self, content):
        self.content = content

    def on_finish(self):
        pass

    @asynchronous
    def get(self, *args, **kwargs):
        try:
            self.set_header('Content-Type', 'application/json')

            locale = self.get_argument("locale", None)
            raw_page = self.get_argument("page", None)
            raw_page_size = self.get_argument("page_size", None)
            raw_context = self.get_argument("context", None)

            if raw_page is None:
                self.set_status(412)
                self.finish(
                    {
                        "status": "error",
                        "message": "missing param=page"
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
                page = int(raw_page)
                page_size = int(raw_page_size)
                context = json_decode(url_unescape(raw_context))
                suggestions = self.suggest(context, page, page_size)

                self.set_status(200)
                self.finish(
                    {
                        "suggestions": suggestions,
                        "version": "0.0.1"
                    }
                )

                # TODO Log stuff here

        except Exception as e:
            app_log.error("error=%s" % e)
            self.set_status(500)
            self.finish(
                {
                    "status": "error"
                }
            )

    def get_content_list_response(self, _type, key):
        if _type in ["popular", "added"]:
            url = "%s/%s.json" % (CONTEXT_URL, _type)
        else:
            url = "%s%s/%s.json" % (CONTEXT_URL, _type, key)

        return self.content.get_reason_list(url)

    def suggest(self, context, page, page_size):
        reasons = defaultdict(list)
        scores = defaultdict(int)

        for entity in context["entities"]:
            response = self.get_content_list_response(
                entity["type"],
                entity["key"]
            )
            self.process_scores(
                response,
                entity["type"],
                entity["key"],
                "detection",
                reasons,
                scores,
                entity["weighting"]
            )

        sorted_scores = sorted(scores.items(), key=lambda y: y[1], reverse=True)
        minimum = sorted_scores[-1][1]
        maximum = sorted_scores[0][1]
        start = (page-1) * page_size
        end = page * page_size
        items_to_return = []
        for x in sorted_scores[start:end]:
            items_to_return.append(
                {
                    "score": (x[1] - minimum) / (maximum - minimum),
                    "_id": x[0]
                }
            )

        return items_to_return

    def process_scores(self, response, _type, key, source, reasons, scores, weighting):
        for x in response:
            scores[x["_id"]] += x["score"] * weighting

    # def suggest(self, context, page, page_size):
    #     _id_reasons = {}
    #     self.process_response(
    #         self.content.get_reason_list(
    #             "%s/popular.json" % CONTEXT_URL
    #         ),
    #         "popular", "popular", "inferred", _id_reasons
    #     )
    #     entities_to_use = [x for x in context["entities"] if x["type"] in ["color", "theme", "style"]]
    #     for entity in entities_to_use:
    #         response = self.content.get_reason_list(
    #             "%s%s/%s.json" % (CONTEXT_URL, entity["type"], entity["key"])
    #         )
    #         self.process_response(response, entity["type"], entity["key"], "detection", _id_reasons)
    #
    #     sorted_suggestions = sorted(_id_reasons.values(), key=itemgetter("score"), reverse=True)
    #     minimum = sorted_suggestions[-1]["score"]
    #     maximum = sorted_suggestions[0]["score"]
    #     start = (page-1) * page_size
    #     end = page * page_size
    #     return list(self.fill(sorted_suggestions[start:end], minimum, maximum))
    #
    # def process_response(self, response, _type, key, source, _id_reasons):
    #     for x in response:
    #         reason = {
    #             "source": source,
    #             "type": _type,
    #             "key": key,
    #             "score": x["score"]
    #         }
    #         if x["_id"] in _id_reasons:
    #             _id_reasons[x["_id"]]["reasons"].append(reason)
    #             _id_reasons[x["_id"]]["score"] += reason["score"]
    #         else:
    #             _id_reasons[x["_id"]] = {
    #                 "reasons": [reason],
    #                 "score": reason["score"],
    #                 "_id": x["_id"]
    #             }

    # def normalise_score(self, suggestions_to_fill, minimum, maximum):
    #     for x in suggestions_to_fill:
    #         x["score"] = (x["score"] - minimum) / (maximum - minimum)
    #         yield x
