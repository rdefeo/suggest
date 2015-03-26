import logging
from suggest.data.data import Data

__author__ = 'robdefeo'


class Suggestion(Data):
    LOGGER = logging.getLogger(__name__)
    collection_name = "suggestions"

    def insert(self, items, locale, context_id, session_id, page, page_size):
        self.collection.insert(
            {
                "items": items,
                "locale": locale,
                "context_id": context_id,
                "session_id": session_id,
                "page": page,
                "page_size": page_size
            }
        )