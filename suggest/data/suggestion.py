import logging
from bson import ObjectId
from suggest.data.data import Data
from datetime import datetime
from suggest import __version__
__author__ = 'robdefeo'


class Suggestion(Data):
    LOGGER = logging.getLogger(__name__)
    collection_name = "suggestion"

    def insert(self, items, locale, context_id, user_id, application_id, session_id, offset, page_size, now=None):
        if now is None:
            now = datetime.now()

        for index, x in enumerate(items):
            x["index"] = index
            x["_id"] = ObjectId(x["_id"])
        data = {
            "items": [
                {
                    "index": index,
                    "_id": x["_id"],
                    "reasons": x["reasons"],
                    "score": x["score"]
                } for index, x in enumerate(items)
            ],
            "locale": locale,
            "application_id": application_id,
            "context_id": context_id,
            "session_id": session_id,
            "offset": offset,
            "page_size": page_size,
            "created": now.isoformat(),
            "version": __version__
        }
        if user_id is not None:
            data["user_id"] = user_id

        self.collection.insert(data)