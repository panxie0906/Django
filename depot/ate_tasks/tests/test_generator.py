from django.test import TestCase

from ate_tasks.views import ValidationPhaseViewGenerator


class BaseGeneratorTest(TestCase):
    def test_generator(self):
        validation = ValidationPhaseViewGenerator()
        a = 10
