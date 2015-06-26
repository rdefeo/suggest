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


class weight_scores_Tests(TestCase):
    maxDiff = None

    def test_first_page(self):
        content = Mock()
        target = Target(content)
        actual = target.weight_scores(
            [
                ("2", {"score": 14, "reasons": "reasons_value"}),
                ("4", {"score": 12, "reasons": "reasons_value"}),
                ("6", {"score": 12, "reasons": "reasons_value"}),
                ("5", {"score": 5, "reasons": "reasons_value"}),
                ("1", {"score": 4, "reasons": "reasons_value"}),
                ("3", {"score": 2, "reasons": "reasons_value"})
            ],
            0,
            5
        )
        self.assertListEqual(
            actual,
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
                }
            ]
        )

    def test_last_page(self):
        content = Mock()
        target = Target(content)
        actual = target.weight_scores(
            [
                ("2", {"score": 14, "reasons": "reasons_value"}),
                ("4", {"score": 12, "reasons": "reasons_value"}),
                ("6", {"score": 12, "reasons": "reasons_value"}),
                ("5", {"score": 5, "reasons": "reasons_value"}),
                ("1", {"score": 4, "reasons": "reasons_value"}),
                ("3", {"score": 2, "reasons": "reasons_value"})
            ],
            4,
            5
        )
        self.assertListEqual(
            actual,
            [
                {
                    'index': 4, 'reasons': 'reasons_value', '_id': '1', 'score': 16.666666666666664
                },
                {
                    'index': 5, 'reasons': 'reasons_value', '_id': '3', 'score': 0.0
                }
            ]
        )

    def test_past_last_page(self):
        content = Mock()
        target = Target(content)
        actual = target.weight_scores(
            [
                ("2", {"score": 14, "reasons": "reasons_value"}),
                ("4", {"score": 12, "reasons": "reasons_value"}),
                ("6", {"score": 12, "reasons": "reasons_value"}),
                ("5", {"score": 5, "reasons": "reasons_value"}),
                ("1", {"score": 4, "reasons": "reasons_value"}),
                ("3", {"score": 2, "reasons": "reasons_value"})
            ],
            10,
            5
        )
        self.assertListEqual(
            actual,
            []
        )


class get_suggestion_response_Tests(TestCase):
    maxDiff = None

    def test_no_scores(self):
        content = Mock()
        target = Target(content)
        target.get_scores = Mock()
        target.get_scores.return_value = {}
        target.get_reason_summary = Mock()
        target.get_reason_summary.return_value = "reason_summary_value"
        target.weight_scores = Mock()
        target.weight_scores.return_value = "weighted_scores_value"
        target.sort_scores = Mock()
        target.sort_scores.return_value = "sort_scores_value"

        actual = target.get_suggestion_response(
            "context",
            0,
            10
        )
        self.assertDictEqual(
            actual,
            {
                'suggestions': 'weighted_scores_value',
                'reasons': 'reason_summary_value',
                'version': '0.0.2',
                'total_suggestions_count': 0
            }
        )

        self.assertEqual(
            target.get_scores.call_count,
            1
        )
        self.assertEqual(
            target.get_scores.call_args_list[0][0][0],
            "context"
        )

        self.assertEqual(
            target.get_reason_summary.call_count,
            1
        )
        self.assertDictEqual(
            target.get_reason_summary.call_args_list[0][0][0],
            {}
        )

        self.assertEqual(
            target.weight_scores.call_count,
            1
        )
        self.assertEqual(
            target.weight_scores.call_args_list[0][0][0],
            'sort_scores_value'
        )
        self.assertEqual(
            target.weight_scores.call_args_list[0][0][1],
            0
        )
        self.assertEqual(
            target.weight_scores.call_args_list[0][0][1],
            0
        )

    def test_has_scores(self):
        content = Mock()
        target = Target(content)
        target.get_reason_summary = Mock()
        target.get_reason_summary.return_value = "reason_summary_value"
        target.weight_scores = Mock()
        target.weight_scores.return_value = "weighted_scores_value"
        target.get_scores = Mock()
        target.get_scores.return_value = ["score_1", "score_2"]
        target.sort_scores = Mock()
        target.sort_scores.return_value = "sort_scores_value"

        actual = target.get_suggestion_response(
            "context",
            0,
            10
        )

        self.assertDictEqual(
            actual,
            {
                'version': '0.0.2',
                'suggestions': 'weighted_scores_value',
                'reasons': 'reason_summary_value',
                'total_suggestions_count': 2
            }
        )

        self.assertEqual(
            target.get_scores.call_count,
            1
        )
        self.assertEqual(
            target.get_scores.call_args_list[0][0][0],
            "context"
        )
        self.assertEqual(
            target.get_reason_summary.call_count,
            1
        )

        self.assertEqual(
            target.weight_scores.call_count,
            1
        )
        self.assertEqual(
            target.weight_scores.call_args_list[0][0][0],
            'sort_scores_value'
        )
        self.assertEqual(
            target.weight_scores.call_args_list[0][0][1],
            0
        )
        self.assertEqual(
            target.weight_scores.call_args_list[0][0][1],
            0
        )

        self.assertEqual(
            target.sort_scores.call_count,
            1
        )
        self.assertEqual(
            target.sort_scores.call_args_list[0][0][0],
            ["score_1", "score_2"]
        )


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

        actual = target.get_scores(
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

        actual = target.get_scores(
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
            actual,
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
                }
            }
        )
