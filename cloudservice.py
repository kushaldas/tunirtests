"""
From https://fedoraproject.org/wiki/QA:Testcase_base_service_manipulation.

"""
import unittest
from .testutils import get_fedora_release, system

SERVICE = "chronyd"
if get_fedora_release() == "24":
    SERVICE = "crond"

class TestServiceManipulation(unittest.TestCase):

    def test_service(self):
        "Tests the service."
        statuscmd = 'systemctl status {}.service'.format(SERVICE)
        out, err, eid = system(statuscmd)
        out = out.decode('utf-8')
        self.assertIn('inactive', out)
        system('systemctl start {}.service'.format(SERVICE))
        out, err, eid = system(statuscmd)
        out = out.decode('utf-8')
        self.assertIn('disabled', out)
        system('systemctl stop {}.service'.format(SERVICE))
        out, err, eid = system(statuscmd)
        out = out.decode('utf-8')
        self.assertIn('inactive', out)
        system('systemctl enable {}.service'.format(SERVICE))


class TestServiceAfter(unittest.TestCase):

    def test_service(self):
        "Tests the service."
        out, err, eid = system('systemctl status {}.service'.format(SERVICE))
        out = out.decode('utf-8')
        self.assertIn('active (running)', out)
        system('systemctl disable {}.service'.format(SERVICE))


class TestServiceFinal(unittest.TestCase):

    def test_service(self):
        "Tests the service."
        out, err, eid = system('systemctl status {}.service'.format(SERVICE))
        out = out.decode('utf-8')
        self.assertIn('disabled', out)

class TestServiceStop(unittest.TestCase):

    def test_service(self):
        out, err, eid = system("systemctl stop {}.service".format(SERVICE))
        self.assertEqual(eid, 0, err)

class TestServiceDisable(unittest.TestCase):

    def test_service(self):
        out, err, eid = system("systemctl disable {}.service".format(SERVICE))
        self.assertEqual(eid, 0, err)


if __name__ == '__main__':
    unittest.main()
