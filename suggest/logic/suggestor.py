from collections import defaultdict
from suggest.settings import CONTEXT_URL

__author__ = 'robdefeo'


class Suggestor(object):
    def __init__(self, content):
        self.content = content

    def get_content_list_response(self, _type, key):
        if _type in ["popular", "added"]:
            url = "%s/%s.json" % (CONTEXT_URL, _type)
        else:
            url = "%s%s/%s.json" % (CONTEXT_URL, _type, key)

        return self.content.get_reason_list(url)

    def get_scores(self, context, ):
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
                scores,
                entity["weighting"]
            )

        return scores

    def get_reasons(self, context, suggestions, minimum, maximum):
        reasons = defaultdict(list)
        for entity in context["entities"]:
            response = self.get_content_list_response(
                entity["type"],
                entity["key"]
            )
            for x in response:
                reasons[x["_id"]].append(
                    {
                        "weighting": entity["weighting"],
                        "type": entity["type"],
                        "key": entity["key"],
                        "score": x["score"]
                    }
                )

        suggestion_reasons = []
        for x in suggestions:
            for y in reasons[x["_id"]]:
                y["normalized_weighted"] = (y["score"] * y["weighting"]) / maximum

            suggestion_reasons.append(
                {
                    "reasons": reasons[x["_id"]],
                    "score": x["score"],
                    "_id": x["_id"]
                }
            )

        return suggestion_reasons

    def score_suggestions(self, context, page, page_size):
        scores = self.get_scores(context)
        response = {
            "version": "0.0.1"
        }
        minimum = None
        maximum = None
        if any(scores):
            sorted_scores = sorted(scores.items(), key=lambda y: y[1], reverse=True)
            minimum = sorted_scores[-1][1]
            maximum = sorted_scores[0][1]
            range = maximum - minimum
            start = (page-1) * page_size
            end = page * page_size
            items_to_return = []
            for x in sorted_scores[start:end]:
                items_to_return.append(
                    {
                        "score": (x[1] - minimum) / range if range != 0 else 0.5,
                        "_id": x[0]
                    }
                )

            response["suggestions"] = items_to_return
        else:
            response["suggestions"] = []

        return response, minimum, maximum


    def process_scores(self, response, _type, key, source, scores, weighting):
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