from collections import defaultdict
from operator import itemgetter
from math import log
from suggest.settings import CONTENT_URL

class Suggestor(object):
    def __init__(self, content):
        self.content = content

    def get_content_list_response(self, _type, key):
        if _type in ["popular", "added"]:
            url = "%s%s.json" % (CONTENT_URL, _type)
        else:
            url = "%s%s/%s.json" % (CONTENT_URL, _type, key)

        return self.content.get_reason_list(url)

    def get_scores(self, context):
        scores = defaultdict(lambda: {'score': 0, 'reasons': []})
        for entity in context["entities"]:
            response = self.get_content_list_response(
                entity["type"],
                entity["key"]
            )
            if response is not None:
                for x in response:
                    item_score = x["score"] * (entity["weighting"] / 100)
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
        scoring_modifications.extend(
            self.get_content_list_response(
                "popular",
                None
            )
        )
        scoring_modifications.extend(
            self.get_content_list_response(
                "added",
                None
            )
        )

        for x in scoring_modifications:
            if x["_id"] in scores:
                item_score = log(x["score"])
                scores[x["_id"]]["score"] += item_score
                scores[x["_id"]]["reasons"].append(
                    {
                        "type": "popular",
                        "raw_score": x["score"],
                        "score": item_score
                    }
                )

        return scores


    def get_reason_summary(self, scores):
        summary = defaultdict(lambda: {'count': 0, 'total_score': 0, 'average_score': 0, 'reasons': []})

        for score in scores.values():
            key = "".join(["%s%s" % (x["type"], x["key"]) for x in score["reasons"] if x["type"] not in ["added", "popular"]])
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

        return summary

    def score_suggestions(self, context, offset, page_size):
        scores = self.get_scores(context)
        response = {
            "version": "0.0.1"
        }
        minimum = None
        maximum = None
        if any(scores):
            sorted_scores = sorted(scores.items(), key=lambda y: y[1]['score'], reverse=True)
            minimum = sorted_scores[-1][1]['score']
            maximum = sorted_scores[0][1]['score']
            score_range = maximum - minimum
            start = offset
            end = offset + page_size
            items_to_return = []
            for x in sorted_scores[start:end]:
                items_to_return.append(
                    {
                        "score": (x[1]['score'] - minimum) / score_range if score_range != 0 else 0.5,
                        "_id": x[0],
                        "reasons": x[1]['reasons']
                    }
                )
            reasons = sorted(self.get_reason_summary(scores).values(), key=itemgetter('average_score'), reverse=True)
            response["reasons"] = reasons
            response["suggestions"] = items_to_return
        else:
            response["suggestions"] = []

        return response, minimum, maximum
