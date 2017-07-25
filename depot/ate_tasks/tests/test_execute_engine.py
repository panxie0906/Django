from django.test import TestCase

from ate_tasks.management.commands.run_test_engine import BaseTask


class BaseTaskTest(TestCase):
    def test_wrap_test_record(self):
        _pass = True
        name = 'task'
        detail = 'None'
        expected = {'pass': _pass, 'detail': detail, 'name': name}
        result = BaseTask.wrap_test_record(_pass, detail, name)
        self.assertDictEqual(expected, result)
