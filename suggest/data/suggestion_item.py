from datetime import datetime, timedelta
from logging import getLogger

from bson import ObjectId, Code, SON

from suggest.data.data import Data
from suggest import __version__


class SuggestionItem(Data):
    LOGGER = getLogger(__name__)
    collection_name = "suggestion_item"

    def insert(self, items, locale, application_id,
               session_id, offset: 0, page_size, _id=None, now=None):
        """
        :type page_size: int
        :type session_id: ObjectId
        :type application_id: ObjectId
        :type locale: str
        :type items: list
        """
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

    def map_product_result_listing(self, now=datetime.now(), days_behind=30):
        mapper = Code("""
            function(){
                for(var i in this.items) {
                    var item = this.items[i]
                    emit(
                        {
                            product_id: item._id
                        },
                        {
                            listing_count: 1
                        }
                    )
                }
            }
        """)
        reducer = Code("""
            function(key, values) {
                var total = 0;
                values.forEach(function(value) {
                    total += value.listing_count;
                });

                return {
                    listing_count: total
                };

            }
        """)

        timestamp = (now - timedelta(days=days_behind)).isoformat()

        self.LOGGER.info(
            "generate=product_result_listing,timestamp=%s,out=product_result_listing,action=replace,db=generate",
            timestamp)

        result = self.collection.map_reduce(
            mapper,
            reducer,
            query={
                "created": {
                    "$gte": timestamp
                }
            },
            out=SON(
                [
                    ("replace", "product_result_listing"),
                    ("db", "generate")
                ]
            )

        )

        return result
