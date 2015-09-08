"""
From https://fedoraproject.org/wiki/QA:Testcase_base_service_manipulation.

"""
import unittest
from .testutils import system


class TestServiceManipulation(unittest.TestCase):

    def test_service(self):
        "Tests the crond service."
        out, err, eid = system('systemctl status crond.service')
        out = out.decode('utf-8')
        self.assertIn('inactive', out)
        system('systemctl start crond.service')
        out, err, eid = system('systemctl status crond.service')
        out = out.decode('utf-8')
        self.assertIn('disabled', out)
        system('systemctl stop crond.service')
        out, err, eid = system('systemctl status crond.service')
        out = out.decode('utf-8')
        self.assertIn('inactive', out)
        system('systemctl enable crond.service')


class TestServiceAfter(unittest.TestCase):

    def test_service(self):
        "Tests the crond service."
        out, err, eid = system('systemctl status crond.service')
        out = out.decode('utf-8')
        self.assertIn('active (running)', out)
        system('systemctl disable crond.service')


class TestServiceFinal(unittest.TestCase):

    def test_service(self):
        "Tests the crond service."
        out, err, eid = system('systemctl status crond.service')
        out = out.decode('utf-8')
        self.assertIn('disabled', out)

if __name__ == '__main__':
    unittest.main()
