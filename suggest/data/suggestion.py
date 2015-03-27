import logging
from suggest.data.data import Data
from datetime import datetime
__author__ = 'robdefeo'


class Suggestion(Data):
    LOGGER = logging.getLogger(__name__)
    collection_name = "suggestions"

    def insert(self, items, locale, application_id, context_id, session_id, page, page_size, now=None):
        if now is None:
            now = datetime.now()

        self.collection.insert(
            {
                "items": items,
                "locale": locale,
                "application_id": application_id,
                "context_id": context_id,
                "session_id": session_id,
                "page": page,
                "page_size": page_size,
                "created": now.isoformat()
            }
        )