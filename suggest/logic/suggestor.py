from collections import defaultdict
from operator import itemgetter
from math import log
from bson import ObjectId

from suggest.settings import CONTENT_URL


class Suggestor(object):
    def __init__(self, content):
        self.content = content

    def get_content_list_response(self, _type, key):
        if _type == "non_attribute":
            url = "%s%s.json" % (CONTENT_URL, key)
        else:
            url = "%s%s/%s.json" % (CONTENT_URL, _type, key)

        return self.content.reason_cache(url)

    def score_items(self, context: dict) -> dict:
        scores = defaultdict(lambda: {'_id': None, 'score': 0, 'reasons': []})
        for entity in context["entities"]:
            response = self.get_content_list_response(
                entity["type"],
                entity["key"]
            )
            for x in response if response is not None else []:
                item_score = x["score"] * (entity["weighting"] / 100)
                scores[x["_id"]]["_id"] = ObjectId(x["_id"])
                scores[x["_id"]]["score"] += item_score
                scores[x["_id"]]["reasons"].append(
                    {
                        "weighting": entity["weighting"],
                        "type": entity["type"],
                        "key": entity["key"],
                        "raw_score": x["score"],
                        "score": item_score
                    }
                )

        scoring_modifications = []
        popular = self.get_content_list_response(
            "non_attribute",
            "popular"
        )

        added = self.get_content_list_response(
            "non_attribute",
            "added"
        )

        scoring_modifications.extend(popular if popular is not None else [])
        scoring_modifications.extend(added if added is not None else [])

        for x in scoring_modifications:
            if x["_id"] in scores and x["score"] > 0:
                item_score = log(x["score"])
                scores[x["_id"]]["_id"] = ObjectId(x["_id"])
                scores[x["_id"]]["score"] += item_score
                scores[x["_id"]]["reasons"].append(
                    {
                        "type": "popular",
                        "raw_score": x["score"],
                        "score": item_score
                    }
                )

        return scores

    @staticmethod
    def sort_items(scores: dict) -> list:
        return sorted(scores.values(), key=lambda y: y['score'], reverse=True)

    def create_suggestion_items(self, context):
        scores = self.score_items(context)
        sorted_items = self.sort_items(scores)
        return self.weight_item_scores(sorted_items)

    def get_reason_summary(self, scores):
        summary = defaultdict(lambda: {'count': 0, 'total_score': 0, 'average_score': 0, 'reasons': []})

        for score in scores.values():
            key = "".join(
                ["%s%s" % (x["type"], x["key"]) for x in score["reasons"] if x["type"] not in ["added", "popular"]])
            summary[key]["count"] += 1
            summary[key]["total_score"] += score["score"]
            summary[key]["average_score"] = summary[key]["total_score"] / summary[key]["count"]

            summary[key]["reasons"] = [
                {
                    "key": x["key"],
                    "type": x["type"],
                    "score": x["score"]
                } for x in score["reasons"] if x["type"] not in ["added", "popular"]
                ]

        return sorted(summary.values(), key=itemgetter('average_score'), reverse=True)

    # def get_suggestion_response(self, context, offset, page_size):
    #     # TODO remove me
    #     scores = self.get_scores(context)
    #     sorted_scores = self.sort_scores(scores)
    #
    #     return {
    #         "version": __version__,
    #         "reasons": self.get_reason_summary(scores),
    #         "total_suggestions_count": len(scores),
    #         "suggestions": self.weight_scores(sorted_scores, offset, page_size)
    #     }

    @staticmethod
    def weight_item_scores(sorted_scores: list):
        items_to_return = []
        minimum = sorted_scores[-1]['score'] if any(sorted_scores) else 0
        maximum = sorted_scores[0]['score'] if any(sorted_scores) else 0
        score_range = maximum - minimum

        for index, x in enumerate(sorted_scores):
            items_to_return.append(
                {
                    "score": float(float((x['score'] - minimum) / score_range) * 100 if score_range != 0 else 50),
                    "_id": x['_id'],
                    "reasons": x['reasons'],
                    "index": index
                }
            )

        return items_to_return

    # def weight_scores(self, sorted_scores: list, offset, page_size):
    #     items_to_return = []
    #     if any(sorted_scores):
    #         minimum = sorted_scores[-1]['score']
    #         maximum = sorted_scores[0]['score']
    #         score_range = maximum - minimum
    #         start = offset
    #         end = offset + page_size
    #
    #         for index, x in enumerate(sorted_scores[start:end]):
    #             items_to_return.append(
    #                 {
    #                     "score": float(
    #                         float((x['score'] - minimum) / score_range) * 100 if score_range != 0 else 50),
    #                     "_id": x['_id'],
    #                     "reasons": x['reasons'],
    #                     "index": index + offset
    #                 }
    #             )
    #
    #     return items_to_return
