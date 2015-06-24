from bson import ObjectId

__author__ = 'robdefeo'
from unittest import TestCase
from mock import Mock
from datetime import datetime
from suggest.data.suggestion import Suggestion as Target


class insert_Test(TestCase):
    maxDiff = None

    def test_regular(self):
        target = Target()
        target.collection = Mock()
        target.insert(
            [
                {
                    "key": "1",
                    "value": "1_value",
                    "_id": "55194a387d391b7e56bd75ed",
                    "reasons": "reasons_value",
                    "score": 1
                },
                {
                    "key": "2",
                    "value": "2_value",
                    "_id": "55194a387d391b7e56bd75ef",
                    "reasons": "reasons_value",
                    "score": 0.75
                },
                {
                    "key": "3",
                    "value": "3_value",
                    "_id": "55194a387d391b7e56bd75e1",
                    "reasons": "reasons_value",
                    "score": 0.5
                }
            ],
            "locale_value",
            "context_id_value",
            "user_id_value",
            "application_id_value",
            "session_id_value",
            0,
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
                'locale': 'locale_value',
                'offset': 0,
                'page_size': 10,
                'session_id': 'session_id_value',
                'user_id': 'user_id_value',
                'version': '0.0.1',
                'items': [
                    {
                        '_id': ObjectId('55194a387d391b7e56bd75ed'),
                        'index': 0,
                        'reasons': 'reasons_value',
                        'score': 1.0
                    },
                    {
                        '_id': ObjectId('55194a387d391b7e56bd75ef'),
                        'index': 1,
                        'reasons': 'reasons_value',
                        'score': 0.75
                    },
                    {
                        '_id': ObjectId('55194a387d391b7e56bd75e1'),
                        'index': 2,
                        'reasons': 'reasons_value',
                        'score': 0.5
                    }
                ]
            }
        )

    def test_none_user_id(self):
        target = Target()
        target.collection = Mock()
        target.insert(
            [
                {
                    "key": "1",
                    "value": "1_value",
                    "_id": "55194a387d391b7e56bd75ed",
                    "reasons": "reasons_value",
                    "score": 1.0
                },
                {
                    "key": "2",
                    "value": "2_value",
                    "_id": "55194a387d391b7e56bd75ef",
                    "reasons": "reasons_value",
                    "score": 0.75
                },
                {
                    "key": "3",
                    "value": "3_value",
                    "_id": "55194a387d391b7e56bd75e1",
                    "reasons": "reasons_value",
                    "score": 0.5
                }
            ],
            "locale_value",
            "context_id_value",
            None,
            "application_id_value",
            "session_id_value",
            0,
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
                'items': [
                    {
                        '_id': ObjectId('55194a387d391b7e56bd75ed'),
                        'index': 0,
                        'reasons': 'reasons_value',
                        'score': 1.0},
                    {
                        '_id': ObjectId('55194a387d391b7e56bd75ef'),
                        'index': 1,
                        'reasons': 'reasons_value',
                        'score': 0.75
                    },
                    {
                        '_id': ObjectId('55194a387d391b7e56bd75e1'),
                        'index': 2,
                        'reasons': 'reasons_value',
                        'score': 0.5
                    }
                ],
                'locale': 'locale_value',
                'offset': 0,
                'page_size': 10,
                'session_id': 'session_id_value',
                'version': '0.0.2'
            }
        )