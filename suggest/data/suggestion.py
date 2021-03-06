from datetime import datetime

from logging import getLogger

from bson import ObjectId

from pylru import lrucache

from suggest.data.data import Data
from suggest import __version__
from suggest.settings import DATA_CACHE_SIZE_SUGGESTION

MAX_SUGGESTIONS_STORED = 1000


class Suggestion(Data):
    LOGGER = getLogger(__name__)
    collection_name = "suggestion"
    cache = lrucache(DATA_CACHE_SIZE_SUGGESTION)

    def get(self, _id=None):
        if _id in self.cache:
            return self.cache[_id]
        else:
            data = next(self.collection.find({"_id": _id}), None)
            self.cache[_id] = data
            return data

    def insert(self, items, locale, context, user_id, application_id,
               session_id, _id=None, now=None):
        """
        :type session_id: ObjectId
        :type application_id: ObjectId
        :type user_id: ObjectId
        :type context: dict
        :type items: list
        """
        if now is None:
            now = datetime.now()

        _id = ObjectId() if _id is None else _id

        data = {
            "_id": _id,
            "items_length": len(items),
            "items": items[:MAX_SUGGESTIONS_STORED],
            "locale": locale,
            "application_id": application_id,
            "context": context,
            "session_id": session_id,
            "created": now.isoformat(),
            "version": __version__
        }
        if user_id is not None:
            data["user_id"] = user_id

        self.collection.insert(data)

        self.cache[_id] = data

        return _id
