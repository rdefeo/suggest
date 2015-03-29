__author__ = 'robdefeo'
from unittest import TestCase
from mock import Mock
from datetime import datetime
from suggest.data.suggestion import Suggestion as Target


class insert_Test(TestCase):
    def test_regular(self):
        target = Target()
        target.collection = Mock()
        target.insert(
            "items_value",
            "locale_value",
            "context_id_value",
            "user_id_value",
            "application_id_value",
            "session_id_value",
            1,
            10,
            datetime(2010, 1, 1)
        )

        self.assertEqual(
            target.collection.insert.call_count,
            1
        )
        self.assertDictEqual(
            target.collection.insert.call_args_list[0][0][0],
            {
                'application_id': 'application_id_value',
                'context_id': 'context_id_value',
                'created': '2010-01-01T00:00:00',
                'items': 'items_value',
                'locale': 'locale_value',
                'page': 1,
                'page_size': 10,
                'session_id': 'session_id_value',
                'user_id': 'user_id_value',
                'version': '0.0.1'
            }
        )

    def test_none_user_id(self):
        target = Target()
        target.collection = Mock()
        target.insert(
            "items_value",
            "locale_value",
            "context_id_value",
            None,
            "application_id_value",
            "session_id_value",
            1,
            10,
            datetime(2010, 1, 1)
        )

        self.assertEqual(
            target.collection.insert.call_count,
            1
        )
        self.assertDictEqual(
            target.collection.insert.call_args_list[0][0][0],
            {
                'application_id': 'application_id_value',
                'context_id': 'context_id_value',
                'created': '2010-01-01T00:00:00',
                'items': 'items_value',
                'locale': 'locale_value',
                'page': 1,
                'page_size': 10,
                'session_id': 'session_id_value',
                'version': '0.0.1'
            }
        )