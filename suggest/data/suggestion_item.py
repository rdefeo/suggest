from datetime import datetime
from logging import getLogger
from bson import ObjectId
from suggest.data.data import Data
from suggest import __version__


class SuggestionItem(Data):
    LOGGER = getLogger(__name__)
    collection_name = "suggestion_item"

    def insert(self, items: list, locale: str, application_id: ObjectId,
               session_id: ObjectId, offset: 0, page_size: int, _id=None, now=None):
        now = datetime.now() if now is None else now
        _id = ObjectId() if _id is None else _id

        data = {
            "_id": _id,
            "page_size": page_size,
            "session_id": session_id,
            "items": items,
            "created": now.isoformat(),
            "version": __version__,
            "locale": locale,
            "application_id": application_id,
            "offset": offset
        }

        self.collection.insert(data)

        return _id
