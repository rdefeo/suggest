import logging
from datetime import datetime, timedelta

from bson import ObjectId
from bson.code import Code
from bson.son import SON
from pylru import lrucache

from suggest.data.data import Data
from suggest import __version__
from suggest.settings import DATA_CACHE_SIZE_SUGGESTION


class Suggestion(Data):
    LOGGER = logging.getLogger(__name__)
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

    # TODO #39 need to be moved somewhere else entirely
    def map_product_result_listing(self, now=datetime.now(), days_behind=30):
        """
        Used to get the more displayed results
        :param _id_type_list: which types to consider in detection
        :return:
        """

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

        self.LOGGER.info("generate=product_result_listing,timestamp=%s,out=product_result_listing,action=replace,db=generate", timestamp)

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

