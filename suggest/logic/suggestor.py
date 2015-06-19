from collections import defaultdict
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
        # scores = defaultdict(int)
        scores = defaultdict(lambda: {'score': 0, 'reasons':[]})
        for entity in context["entities"]:
            response = self.get_content_list_response(
                entity["type"],
                entity["key"]
            )
            if response is not None:
                for x in response:
                    scores[x["_id"]]["score"] += x["score"] * entity["weighting"]
                    scores[x["_id"]]["reasons"].append(
                        {
                            "weighting": entity["weighting"],
                            "type": entity["type"],
                            "key": entity["key"],
                            "score": x["score"],
                            "weighted_score": x["score"] * entity["weighting"]
                        }
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

            response["suggestions"] = items_to_return
        else:
            response["suggestions"] = []

        return response, minimum, maximum
