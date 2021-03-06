from bson import ObjectId

__author__ = 'robdefeo'
from unittest import TestCase
from mock import Mock
from datetime import datetime
from suggest.data.suggestion import Suggestion as Target


class get_Test(TestCase):
    def test_regular(self):
        target = Target()
        target.cache.clear()
        target.collection = Mock()
        target.collection.find.return_value = ["found_value"].__iter__()
        actual = target.get(
            _id="id_value"
        )
        self.assertEquals(1, target.collection.find.call_count)
        self.assertDictEqual(
            {'_id': 'id_value'},
            target.collection.find.call_args_list[0][0][0]
        )

        self.assertEquals("found_value", actual)

    def test_empty(self):
        target = Target()
        target.cache.clear()
        target.collection = Mock()
        target.collection.find.return_value = [].__iter__()
        actual = target.get(
            _id="id_value"
        )
        self.assertEquals(1, target.collection.find.call_count)
        self.assertDictEqual(
            {'_id': 'id_value'},
            target.collection.find.call_args_list[0][0][0]
        )

        self.assertIsNone(actual)

class insert_Test(TestCase):
    maxDiff = None

    def test_regular(self):
        target = Target()
        target.collection = Mock()
        actual = target.insert(
            "items_value",
            "locale_value",
            "context_value",
            "user_id_value",
            "application_id_value",
            "session_id_value",
            _id=ObjectId('55d39f1c7d391b49e1569fad'),
            now=datetime(2010, 1, 1)
        )

        self.assertEqual(
            ObjectId('55d39f1c7d391b49e1569fad'),
            actual
        )

        self.assertEqual(1, target.collection.insert.call_count)
        self.assertDictEqual(
            {
                '_id': ObjectId('55d39f1c7d391b49e1569fad'),
                'application_id': 'application_id_value',
                'context': 'context_value',
                'created': '2010-01-01T00:00:00',
                'locale': 'locale_value',
                'session_id': 'session_id_value',
                'user_id': 'user_id_value',
                'version': '0.0.3',
                'items': "items_value",
                'items_length': 11
            },
            target.collection.insert.call_args_list[0][0][0]
        )

    def test_none_user_id(self):
        target = Target()
        target.collection = Mock()
        actual = target.insert(
            "items_value",
            "locale_value",
            "context_value",
            None,
            "application_id_value",
            "session_id_value",
            _id=ObjectId('55d39f1c7d391b49e1569fad'),
            now=datetime(2010, 1, 1)
        )

        self.assertEqual(
            ObjectId('55d39f1c7d391b49e1569fad'),
            actual
        )
        self.assertEqual(1, target.collection.insert.call_count)
        self.assertDictEqual(
            {
                '_id': ObjectId('55d39f1c7d391b49e1569fad'),
                'application_id': 'application_id_value',
                'context': 'context_value',
                'created': '2010-01-01T00:00:00',
                'items': "items_value",
                'items_length': 11,
                'locale': 'locale_value',
                'session_id': 'session_id_value',
                'version': '0.0.3'
            },
            target.collection.insert.call_args_list[0][0][0]
        )
