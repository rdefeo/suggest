import logging
from bson import ObjectId
from suggest.data.data import Data
from datetime import datetime
from suggest import __version__
from bson.code import Code
from bson.son import SON
from datetime import datetime, timedelta

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
                "type": "results",
                "timestamp": {
                    "$gte": timestamp
                }
            },
            out=SON(
                [
                    ("create", "product_result_listing"),
                    ("db", "generate")
                ]
            )

        )

        return result

