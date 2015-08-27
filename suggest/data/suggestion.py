from datetime import datetime

from logging import getLogger

from bson import ObjectId

from pylru import lrucache

from suggest.data.data import Data
from suggest import __version__
from suggest.settings import DATA_CACHE_SIZE_SUGGESTION


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

    def insert(self, items: list, locale, context: dict, user_id: ObjectId, application_id: ObjectId,
               session_id: ObjectId, _id=None, now=None):
        if now is None:
            now = datetime.now()

        _id = ObjectId() if _id is None else _id

        data = {
            "_id": _id,
            "items": items,
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
