from pylru import FunctionCacheManager
import tornado
import tornado.escape
from tornado.httpclient import HTTPClient, HTTPError
from datetime import datetime, timedelta


class Content(object):
    def __init__(self, cache_maxsize=128):
        self.reason_cache = FunctionCacheManager(self.get_reason_list, cache_maxsize)

    def clear(self):
        self.reason_cache.clear()

    def get_reason_list(self, url, max_age_days=3):
        try:
            http_client = HTTPClient()
            response = http_client.fetch(url)
            data = tornado.escape.json_decode(response.body)

            min_created_date_allowed = (datetime.now() - timedelta(days=max_age_days)).isoformat()
            if data["created"] < min_created_date_allowed:
                return None
            else:
                return data["results"]
        except HTTPError as e:
            print("Error=%s,url=%s" % (str(e), url))