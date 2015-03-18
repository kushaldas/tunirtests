"""
From https://fedoraproject.org/wiki/QA:Testcase_base_service_manipulation.

"""
import unittest
from testutils import system


class TestServiceManipulation(unittest.TestCase):

    def test_service(self):
        "Tests the crond service."
        out, err, eid = system('systemctl status crond.service')
        self.assertIn('not running', out)
        system('systemctl start crond.service')
        out, err, eid = system('systemctl status crond.service')
        self.assertIn('Disabled but active', out)
        system('systemctl stop crond.service')
        out, err, eid = system('systemctl status crond.service')
        self.assertIn('not running', out)
        system('systemctl enable crond.service')


class TestServiceAfter(unittest.TestCase):

    def test_service(self):
        "Tests the crond service."
        out, err, eid = system('systemctl status crond.service')
        self.assertIn('active (running)', out)
        system('systemctl disable crond.service')


if __name__ == '__main__':
    unittest.main()