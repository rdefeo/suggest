from functools import lru_cache
import tornado
from tornado.httpclient import HTTPClient

__author__ = 'robdefeo'

@lru_cache(maxsize=128)
def get_list(attribute_type, attribute_key):
    'Retrieve text of a Python Enhancement Proposal'
    url = "http://content.jemboo.com/suggest/%s/%s.json" % (attribute_type, attribute_key)
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return tornado.escape.json_decode(response.body)["results"]