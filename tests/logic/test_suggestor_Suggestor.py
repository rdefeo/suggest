__author__ = 'robdefeo'
from unittest import TestCase
from mock import Mock
from suggest.logic.suggestor import Suggestor as Target


class score_suggestions_Tests(TestCase):
    def test_has_entities(self):
        content = Mock()
        target = Target(content)
        actual = target.score_suggestions(
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