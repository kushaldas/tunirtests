import unittest
import re
from .testutils import system, if_atomic, if_netname_traditional


class TestBase(unittest.TestCase):


    def test_selinux(self):
        "Tests the SELinux"
        out, err, eid = system('sudo getenforce')
        out = out.strip()
        out = out.decode('utf-8')
        self.assertEqual(out, 'Enforcing')

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

# https://github.com/kushaldas/tunirtests/issues/29
@unittest.skipIf(not if_netname_traditional(), "Image is using predictable naming convention.")
class Testnetname(unittest.TestCase):
    "If traditional net naming is turned on, we should see eth0 structures here"
    def test_net_name(self):
        out, err, eid = system("stat /sys/class/net/eth0/operstate")
        self.assertEqual(eid, 0, err)


class TestJournalWritten(unittest.TestCase):
    """
    Test to check that journal logs get written to disk(/var)
    and make sure that user-uid.journal is not lost on first boot
    the test should run on First Boot
    https://bugzilla.redhat.com/show_bug.cgi?id=1265295
    https://bugzilla.redhat.com/show_bug.cgi?id=1353688
    """

    def test_journal_written(self):

        # Find PID
        out, err, eid = system("systemctl show systemd-journald.service -p MainPID")
        out = out.decode('utf-8')
        pid = out[8:-1]

        # Find UID
        out, err, eid = system("id -u")
        uid = out.decode('utf-8').strip('\n')

        # Journal log
        out, err, eid = system("sudo ls -l /proc/{0}/fd/ | grep journal".format(pid))
        out = out.decode('utf-8')
        err = err.decode('utf-8')

        # Find Machine-ID
        with open('/etc/machine-id', 'r') as f:
            mid = f.read().strip('\n')

        self.assertIn('/var/log/journal/{0}/system.journal'.format(mid), out)
        self.assertIn('/var/log/journal/{0}/user-{1}.journal'.format(mid, uid), out)

class TestJournalWrittenAfterReboot(unittest.TestCase):
    "This test executes the same test TestJournalWritten but After Reboot"

    def test_journal_written_after_reboot(self):
        TestJournalWritten.test_journal_written(self)


if __name__ == '__main__':
    unittest.main()
