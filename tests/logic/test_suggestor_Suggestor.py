__author__ = 'robdefeo'
from unittest import TestCase

from mock import Mock

from suggest.logic.suggestor import Suggestor as Target


class score_suggestions_Tests(TestCase):
    def test_has_entities(self):
        content = Mock()
        target = Target(content)
        actual, minimum, maximum = target.score_suggestions(
            {
                "entities": []
            },
            1,
            10
        )

        self.assertDictEqual(
            actual,
            {
                'suggestions': [],
                'version': '0.0.1'
            }
        )

        self.assertIsNone(minimum)
        self.assertIsNone(maximum)


class get_scores_Tests(TestCase):
    def test_no_entities(self):
        target = Target("content")
        target.get_content_list_response = Mock()

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
                    "score": 1
                },
                {
                    "_id": "2",
                    "score": 1
                }
            ],
            None
        ]

        actual = target.get_scores(
            {
                "entities": [
                    {
                        "type": "color",
                        "key": "black",
                        "weighting": 0.6
                    },
                    {
                        "type": "color",
                        "key": "no_data",
                        "weighting": 0.6
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
                            'score': 1,
                            'type': 'color',
                            'weighted_score': 0.6,
                            'weighting': 0.6
                        }
                    ],
                    'score': 0.6
                },
                '2': {
                    'reasons': [
                        {
                            'key': 'black',
                            'score': 1,
                            'type': 'color',
                            'weighted_score': 0.6,
                            'weighting': 0.6
                        }
                    ],
                    'score': 0.6
                }
            }
        )
