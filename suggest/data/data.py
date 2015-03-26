import logging

from suggest.settings import (MONGODB_DB, MONGODB_HOST, MONGODB_PASSWORD, MONGODB_USER)
from pymongo import MongoClient


class Data(object):
    LOGGER = logging.getLogger(__name__)
    collection = None
    collection_name = None
    client = None

    def __init__(self):
        pass

    def create_db(self, authenticated_against_admin=False):
        authentication_database = "admin" if authenticated_against_admin else MONGODB_DB
        self.client =  MongoClient("mongodb://%s:%s@%s:27017/%s" % (
            MONGODB_USER, MONGODB_PASSWORD, MONGODB_HOST, authentication_database
        ))
        return self.client[MONGODB_DB]

    def open_connection(self, authenticated_against_admin=False):
        if self.collection_name is None:
            raise Exception("no collection name specified")

        self.collection = self.create_db(authenticated_against_admin)[self.collection_name]

    def close_connection(self):
        self.client.close()