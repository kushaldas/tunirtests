import unittest
from .testutils import system, if_atomic


class TestBase(unittest.TestCase):


    def test_selinux(self):
        "Tests the SELinux"
        out, err, eid = system('sudo getenforce')
        out = out.strip()
        out = out.decode('utf-8')
        self.assertEquals(out, 'Enforcing')

    def test_logging(self):
        "Tests journald logging"
        out, err, eid = system('sudo journalctl -a --no-pager -r --since=$(date +%Y-%m-%d) -n1')
        out = out.decode('utf-8')
        self.assertGreater(len(out.split()), 3, "journalctl output is missing.")

    def test_services(self):
        "No service should fail in the startup."
        out, err, eid = system('systemctl --all --failed')
        out = out.decode('utf-8')
        self.assertIn('0 loaded units listed', out)

    @unittest.skipIf(if_atomic(), "It is an Atomic image.")
    def test_packageinstall(self):
        "Tests package install using dnf"
        system('dnf install pss -y')
        out, err, eid = system('ls -l /usr/bin/pss')
        self.assertEqual(eid, 0, err)

# https://github.com/kushaldas/tunirtests/issues/17
class TestCloudtmp(unittest.TestCase):
    "/tmp should always be writable."

    def test_write_tmp(self):
        "/tmp should always be writable."
        with open('/tmp/hoo-ha.txt', 'w') as fobj:
            fobj.write("Hello")

# https://github.com/kushaldas/tunirtests/issues/17
class Testtmpmount(unittest.TestCase):

    def test_tmp_mount(self):
        out, err, eid = system("stat -L -c '%a' /tmp")
        self.assertEqual(eid, 0, out+err)
        out = out.decode('utf-8')
        self.assertEqual(out.strip(), '1777')





if __name__ == '__main__':
    unittest.main()
