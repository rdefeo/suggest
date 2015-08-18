__author__ = 'robdefeo'
from unittest import TestCase

from mock import Mock

from suggest.logic.suggestor import Suggestor as Target


class get_reason_summary_Tests(TestCase):
    maxDiff = None

    def test_no_scores(self):
        content = Mock()
        target = Target(content)

        actual = target.get_reason_summary(
            {

            }
        )

        self.assertListEqual(
            actual,
            []
        )

    def test_scores_multiple_reason(self):
        content = Mock()
        target = Target(content)

        actual = target.get_reason_summary(
            {
                '1': {
                    'reasons': [
                        {
                            'key': 'black',
                            'score': 60.0,
                            'type': 'color',
                            'raw_score': 100,
                            'weighting': 60.0
                        },
                        {
                            'raw_score': 50,
                            'score': 3.912023005428146,
                            'type': 'popular'
                        }
                    ],
                    'score': 63.912023005428146
                },
                '2': {
                    'reasons': [
                        {
                            'key': 'black',
                            'score': 60.0,
                            'type': 'color',
                            'raw_score': 100,
                            'weighting': 60.0
                        },
                        {
                            'raw_score': 20,
                            'score': 2.995732273553991,
                            'type': 'popular'
                        }
                    ],
                    'score': 62.99573227355399
                },
                '3': {
                    'reasons': [
                        {
                            'key': 'black',
                            'score': 60.0,
                            'type': 'color',
                            'raw_score': 100,
                            'weighting': 60.0
                        },
                        {
                            'raw_score': 20,
                            'score': 2.995732273553991,
                            'type': 'popular'
                        }
                    ],
                    'score': 60.99573227355399
                },
                '4': {
                    'reasons': [
                        {
                            'key': 'red',
                            'score': 60.0,
                            'type': 'color',
                            'raw_score': 100,
                            'weighting': 60.0
                        },
                        {
                            'raw_score': 20,
                            'score': 4.995732273553991,
                            'type': 'popular'
                        }
                    ],
                    'score': 64.99573227355399
                },
                '5': {
                    'reasons': [
                        {
                            'key': 'red',
                            'score': 60.0,
                            'type': 'color',
                            'raw_score': 100,
                            'weighting': 60.0
                        },
                        {
                            'key': 'black',
                            'score': 60.0,
                            'type': 'color',
                            'raw_score': 100,
                            'weighting': 60.0
                        },
                        {
                            'raw_score': 20,
                            'score': 4.995732273553991,
                            'type': 'popular'
                        }
                    ],
                    'score': 124.99573227355399
                }
            }
        )

        self.assertListEqual(
            actual,
            [
                {
                    'average_score': 124.99573227355398,
                    'count': 1,
                    'reasons': [
                        {
                            'key': 'red', 'score': 60.0, 'type': 'color'
                        },
                        {
                            'key': 'black', 'score': 60.0, 'type': 'color'
                        }
                    ],
                    'total_score': 124.99573227355398
                },
                {
                    'average_score': 64.99573227355398,
                    'count': 1,
                    'reasons': [
                        {
                            'key': 'red', 'score': 60.0, 'type': 'color'
                        }
                    ],
                    'total_score': 64.99573227355398
                },
                {
                    'average_score': 62.634495850845376,
                    'count': 3,
                    'reasons': [
                        {
                            'key': 'black', 'score': 60.0, 'type': 'color'
                        }
                    ],
                    'total_score': 187.90348755253612
                }
            ]
        )

    def test_scores_single_reason(self):
        content = Mock()
        target = Target(content)

        actual = target.get_reason_summary(
            {
                '1': {
                    'reasons': [
                        {
                            'key': 'black',
                            'score': 60.0,
                            'type': 'color',
                            'raw_score': 100,
                            'weighting': 60.0
                        },
                        {
                            'raw_score': 50,
                            'score': 3.912023005428146,
                            'type': 'popular'
                        }
                    ],
                    'score': 63.912023005428146
                },
                '2': {
                    'reasons': [
                        {
                            'key': 'black',
                            'score': 60.0,
                            'type': 'color',
                            'raw_score': 100,
                            'weighting': 60.0
                        },
                        {
                            'raw_score': 20,
                            'score': 2.995732273553991,
                            'type': 'popular'
                        }
                    ],
                    'score': 62.99573227355399
                },
                '3': {
                    'reasons': [
                        {
                            'key': 'black',
                            'score': 60.0,
                            'type': 'color',
                            'raw_score': 100,
                            'weighting': 60.0
                        },
                        {
                            'raw_score': 20,
                            'score': 4.995732273553991,
                            'type': 'popular'
                        }
                    ],
                    'score': 64.99573227355399
                }
            }
        )

        self.assertListEqual(
            actual,
            [
                {
                    'average_score': 63.967829184178704,
                    'count': 3,
                    'reasons': [
                        {
                            'key': 'black', 'score': 60.0, 'type': 'color'
                        }
                    ],
                    'total_score': 191.90348755253612
                }
            ]
        )


class weight_item_scores_Tests(TestCase):
    maxDiff = None

    def test_regular(self):
        content = Mock()
        target = Target(content)
        actual = target.weight_item_scores(
            [
                {"_id": "2", "score": 14, "reasons": "reasons_value"},
                {"_id": "4", "score": 12, "reasons": "reasons_value"},
                {"_id": "6", "score": 12, "reasons": "reasons_value"},
                {"_id": "5", "score": 5, "reasons": "reasons_value"},
                {"_id": "1", "score": 4, "reasons": "reasons_value"},
                {"_id": "3", "score": 2, "reasons": "reasons_value"}
            ]
        )
        self.assertListEqual(
            [
                {
                    'index': 0, '_id': '2', 'reasons': 'reasons_value', 'score': 100.0
                },
                {
                    'reasons': 'reasons_value', '_id': '4', 'index': 1, 'score': 83.33333333333334
                },
                {
                    '_id': '6', 'index': 2, 'reasons': 'reasons_value', 'score': 83.33333333333334
                },
                {
                    'reasons': 'reasons_value', '_id': '5', 'index': 3, 'score': 25.0
                },
                {
                    'reasons': 'reasons_value', '_id': '1', 'index': 4, 'score': 16.666666666666664
                },
                {'_id': '3', 'reasons': 'reasons_value', 'index': 5, 'score': 0.0}
            ],
            actual
        )

    def test_empty(self):
        content = Mock()
        target = Target(content)
        actual = target.weight_item_scores([])
        self.assertListEqual([], actual)


class create_suggestion_Tests(TestCase):
    maxDiff = None

    def test_no_scores(self):
        content = Mock()
        target = Target(content)
        target.score_items = Mock()
        target.score_items.return_value = {}
        target.get_reason_summary = Mock()
        target.get_reason_summary.return_value = "reason_summary_value"
        target.weight_item_scores = Mock()
        target.weight_item_scores.return_value = "weighted_scores_value"
        target.sort_items = Mock()
        target.sort_items.return_value = "sort_scores_value"

        actual = target.create_suggestion_items("context")

        self.assertEqual(
            "weighted_scores_value",
            actual
        )

        self.assertEqual(1, target.score_items.call_count)
        self.assertEqual("context", target.score_items.call_args_list[0][0][0])

        self.assertEqual(1, target.weight_item_scores.call_count)
        self.assertEqual('sort_scores_value', target.weight_item_scores.call_args_list[0][0][0])

    def test_has_scores(self):
        content = Mock()
        target = Target(content)
        target.get_reason_summary = Mock()
        target.get_reason_summary.return_value = "reason_summary_value"
        target.weight_item_scores = Mock()
        target.weight_item_scores.return_value = "weighted_scores_value"
        target.score_items = Mock()
        target.score_items.return_value = ["score_1", "score_2"]
        target.sort_items = Mock()
        target.sort_items.return_value = "sort_scores_value"

        actual = target.create_suggestion_items("context")

        self.assertEqual("weighted_scores_value", actual)

        self.assertEqual(1, target.score_items.call_count)
        self.assertEqual("context", target.score_items.call_args_list[0][0][0])

        self.assertEqual(1, target.weight_item_scores.call_count)
        self.assertEqual('sort_scores_value', target.weight_item_scores.call_args_list[0][0][0])

        self.assertEqual(1, target.sort_items.call_count)
        self.assertEqual(["score_1", "score_2"], target.sort_items.call_args_list[0][0][0])


class get_scores_Tests(TestCase):
    maxDiff = None

    def test_no_entities(self):
        target = Target("content")
        target.get_content_list_response = Mock()
        target.get_content_list_response.side_effect = [
            [],
            [
                {
                    "_id": "1",
                    "score": 1
                },
                {
                    "_id": "2",
                    "score": 1
                }
            ],
            [
                {
                    "_id": "1",
                    "score": 1
                },
                {
                    "_id": "2",
                    "score": 1
                }
            ]
        ]

        actual = target.score_items(
            {
                "entities": []
            }
        )

        self.assertDictEqual(
            actual,
            {}
        )

    def test_none_response_for_one_entity(self):
        target = Target("content")
        target.get_content_list_response = Mock()
        target.get_content_list_response.side_effect = [
            [
                {
                    "_id": "1",
                    "score": 100
                },
                {
                    "_id": "2",
                    "score": 100
                }
            ],
            None,
            [
                {
                    "_id": "1",
                    "score": 50
                },
                {
                    "_id": "4",
                    "score": 100
                }
            ],
            [
                {
                    "_id": "3",
                    "score": 100
                },
                {
                    "_id": "2",
                    "score": 20
                }
            ]
        ]

        actual = target.score_items(
            {
                "entities": [
                    {
                        "type": "color",
                        "key": "black",
                        "weighting": 60.0
                    },
                    {
                        "type": "color",
                        "key": "no_data",
                        "weighting": 60.0
                    }
                ]
            }
        )

        self.assertDictEqual(
            {
                '1': {
                    '_id': '1',
                    'reasons': [
                        {
                            'key': 'black',
                            'score': 60.0,
                            'type': 'color',
                            'raw_score': 100,
                            'weighting': 60.0
                        },
                        {
                            'raw_score': 50,
                            'score': 3.912023005428146,
                            'type': 'popular'
                        }
                    ],
                    'score': 63.912023005428146
                },
                '2': {
                    '_id': '2',
                    'reasons': [
                        {
                            'key': 'black',
                            'score': 60.0,
                            'type': 'color',
                            'raw_score': 100,
                            'weighting': 60.0
                        },
                        {
                            'raw_score': 20,
                            'score': 2.995732273553991,
                            'type': 'popular'
                        }
                    ],
                    'score': 62.99573227355399
                }
            },
            actual
        )
