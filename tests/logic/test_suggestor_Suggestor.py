__author__ = 'robdefeo'
from unittest import TestCase

from mock import Mock

from suggest.logic.suggestor import Suggestor as Target


class score_suggestions_Tests(TestCase):
    maxDiff = None

    def test_no_scores(self):
        content = Mock()
        target = Target(content)
        target.get_scores = Mock()
        target.get_scores.return_value = {}

        actual, minimum, maximum = target.score_suggestions(
            "context",
            0,
            10
        )
        self.assertDictEqual(
            actual,
            {
                'suggestions': [],
                'reasons': [],
                'version': '0.0.2'
            }
        )

    def test_has_scores(self):
        content = Mock()
        target = Target(content)
        target.get_reason_summary = Mock()
        target.get_reason_summary.return_value = "reason_summary_value"
        target.get_scores = Mock()
        target.get_scores.return_value = {
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
            }
        }
        actual, minimum, maximum = target.score_suggestions(
            "context",
            0,
            10
        )

        self.assertDictEqual(
            actual,
            {
                'version': '0.0.2',
                'suggestions': [
                    {
                        'reasons': [
                            {
                                'weighting': 60.0, 'raw_score': 100, 'score': 60.0, 'key': 'black', 'type': 'color'
                            },
                            {
                                'score': 3.912023005428146, 'raw_score': 50, 'type': 'popular'
                            }
                        ],
                        'score': 100.0,
                        '_id': '1'
                    },
                    {
                        'reasons': [
                            {
                                'weighting': 60.0, 'raw_score': 100, 'score': 60.0, 'key': 'black', 'type': 'color'
                            },
                            {
                                'score': 2.995732273553991, 'raw_score': 20, 'type': 'popular'
                            }
                        ],
                        'score': 68.58026801445475,
                        '_id': '2'
                    },
                    {
                        'reasons': [
                            {
                                'weighting': 60.0,
                                'raw_score': 100,
                                'score': 60.0,
                                'key': 'black',
                                'type': 'color'
                            },
                            {
                                'score': 2.995732273553991,
                                'raw_score': 20,
                                'type': 'popular'
                            }
                        ],
                        'score': 0.0, '_id': '3'
                    }
                ],
                'reasons': 'reason_summary_value'
            }
        )

        self.assertEqual(
            60.99573227355399,
            minimum
        )
        self.assertEqual(
            63.912023005428146,
            maximum
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
