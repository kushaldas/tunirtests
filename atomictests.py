import unittest
import re
from .testutils import system, if_atomic


@unittest.skipUnless(if_atomic(), "It's not an atomic image")
class TestAtomicFirstBootRun(unittest.TestCase):

    def test_docker_image_run(self):
        out, err, eid = system(
            'docker run --rm busybox true && echo "PASS"')
        out = out.decode('utf-8')
        self.assertEquals('PASS\n', out)


@unittest.skipUnless(if_atomic(), "It's not an Atomic image")
class TestDockerStorageSetup(unittest.TestCase):

    def test_journalctl_logs(self):
        """Test journalctl logs for docker-storage-setup"""
        out, err, eid = system(
            'journalctl -o cat --unit docker-storage-setup.service'
        )
        out = out.decode('utf-8')
        self.assertTrue(re.search(r'CHANGED: partition=\d', out))
        self.assertTrue(
            re.search(r'Physical volume "/dev/vd[a-z]\d" changed', out))
        self.assertTrue('1 physical volume(s) resized' in out)
        self.assertTrue(
            'Size of logical volume atomicos/root changed from' in out)
        self.assertTrue(
            'Logical volume root successfully resized' in out)
        self.assertTrue('Rounding up size to full physical extent' in out)
        self.assertTrue('Logical volume "docker-meta" created' in out)
        self.assertTrue('Logical volume "docker-data" created' in out)

    def test_lsblk_output(self):
        """Test output for lsblk"""
        out, err, eid = system('sudo lsblk')
        out = out.decode('utf-8')
        self.assertTrue(
            re.search(r'atomicos-root.*\d+(?:.\d+)?G.*lvm.*/sysroot.*\n', out)
        )
        self.assertTrue(
            re.search(r'atomicos-docker--meta.*\d+(?:.\d+)?M.*lvm', out)
        )
        self.assertTrue(
            re.search(r'atomicos-docker--data.*\d+(?:.\d+)?G.*lvm', out)
        )


@unittest.skipUnless(if_atomic(), "It's not an Atomic image")
class TestDockerInstalled(unittest.TestCase):

    def test_run(self):
        out, err, eid = system('rpm -q docker')
        out = out.decode('utf-8')
        self.assertTrue('docker' in out)


@unittest.skipUnless(if_atomic(), "It's not an Atomic image")
class TestAtomicUpgradeRun(unittest.TestCase):

    def test_upgrade_run(self):
        out, err, eid = system('sudo rpm-ostree status')
        out = out.decode('utf-8')
        self.assertTrue(out)
        out, err, eid = system('sudo ostree admin status')
        out = out.decode('utf-8')
        self.assertTrue(out)

        # We create a file /etc/file1 before running rpm-ostree upgrade.
        # This file should persist, even in rolling back the upgrade.
        # This we assert in
        # TestAtomicRollbackPostReboot.test_atomic_rollback_post_reboot
        out, err, eid = system(
            'sudo cat /ostree/repo/refs/heads/ostree/0/1/0 > /etc/file1')
        err = err.decode('utf-8')
        self.assertFalse(err)
        out, err, eid = system('sudo rpm-ostree upgrade')
        err = err.decode('utf-8')
        # Assert successful run
        self.assertFalse(err)


@unittest.skipUnless(if_atomic(), "It's not an Atomic image")
class TestAtomicUpgradePostReboot(unittest.TestCase):

    def test_upgrade_post_reboot(self):
        out, err, eid = system(
            'docker run --rm busybox true && echo "PASS"')
        out = out.decode('utf-8')
        self.assertEquals('PASS\n', out)


@unittest.skipUnless(if_atomic(), "It's not an Atomic image")
class TestAtomicRollbackRun(unittest.TestCase):

    def test_atomic_rollback_run(self):
        # We make changes to the system by creating /etc/file2 before
        # running rollback. Once rollback is run, /etc/file2 will be
        # removed. We assert that in the following test case.
        out, err, eid = system(
            'sudo cat /ostree/repo/refs/heads/ostree/1/1/0 > /etc/file2')
        err = err.decode('utf-8')
        self.assertFalse(err)

        out, err, eid = system('sudo rpm-ostree rollback')
        err = err.decode('utf-8')
        self.assertFalse(err)


@unittest.skipUnless(if_atomic(), "It's not an Atomic image")
class TestAtomicRollbackPostReboot(unittest.TestCase):

    def test_atomic_rollback_post_reboot(self):
        out, err, eid = system('rpm-ostree status')
        out = out.decode('utf-8')
        self.assertTrue(out)

        # Assert that file1 is present
        out, err, eid = system('sudo cat /etc/file1')
        out = out.decode('utf-8')
        self.assertTrue(out)

        # Assert that file2 is not present
        out, err, eid = system('sudo cat /etc/file2')
        err = err.decode('utf-8')
        self.assertTrue(err)

        # Assert that running busybox docker image works after rollback
        out, err, eid = system(
            'docker run --rm busybox true && echo "PASS"')
        out = out.decode('utf-8')
        self.assertEqual(out, 'PASS\n')


@unittest.skipUnless(if_atomic(), "It's not an Atomic image")
class TestAtomicDockerImage(unittest.TestCase):

    def test_docker_image(self):
        out, err, eid = system(
            'curl -O https://dl.fedoraproject.org/pub/alt/stage/23_TC1/Docker'
            '/x86_64/Fedora-Docker-Base-23_TC1-20150929.x86_64.tar.xz')
        out, err, eid = system(
            'sudo docker load -i '
            'Fedora-Docker-Base-23_TC1-20150929.x86_64.tar.xz')
        out, err, eid = system(
            'sudo docker run -it --rm '
            'Fedora-Docker-Base-23_TC1-20150929.x86_64 '
            'true && echo "PASS" || echo "FAIL"')
        out = out.decode('utf-8')
        self.assertEqual(out, 'PASS\n')

if __name__ == '__main__':
    unittest.main()
