mport unittest
import os
import re
import time
from .testutils import system, if_atomic


@unittest.skipUnless(if_atomic(), "It's not an atomic image")
class TestAtomicFirstBootRun(unittest.TestCase):

    def test_docker_image_run(self):
        out, err, eid = system(
            'docker run --rm busybox true && echo "PASS"')
        out = out.decode('utf-8')
        self.assertEqual('PASS\n', out)


@unittest.skipUnless(if_atomic(), "It's not an Atomic image")
class TestDockerStorageSetup(unittest.TestCase):

    def test_journalctl_logs(self):
        """Test journalctl logs for docker-storage-setup"""
        out, err, eid = system(
            'journalctl -o cat --unit docker-storage-setup.service'
        )
        out = out.decode('utf-8')
        print(repr(out))
        self.assertTrue(
            'Started Docker Storage Setup.' in out, out
        )

    def test_lsblk_output(self):
        """Test output for lsblk"""
        out, err, eid = system('sudo lsblk')
        out = out.decode('utf-8')
        self.assertTrue(
            re.search(r'atomicos-root.*\d+(?:.\d+)?G.*lvm.*/sysroot.*\n', out)
        )
        self.assertTrue(
            re.search(r'atomicos-docker--pool_tmeta.*\d+(?:.\d+)?M.*lvm', out)
        )
        self.assertTrue(
            re.search(r'atomicos-docker--pool_tdata.*\d+(?:.\d+)?G.*lvm', out)
        )


@unittest.skipUnless(if_atomic(), "It's not an Atomic image")
class TestDockerInstalled(unittest.TestCase):

    def test_run(self):
        out, err, eid = system('rpm -q docker')
        out = out.decode('utf-8')
        self.assertFalse('not installed' in out, out)


@unittest.skipUnless(if_atomic(), "It's not an Atomic image")
class TestAtomicUpgradeRun(unittest.TestCase):

    def test_upgrade_run(self):
        out, err, eid = system('sudo atomic host status')
        out = out.decode('utf-8')
        self.assertTrue(out)
        out, err, eid = system('sudo ostree admin status')
        out = out.decode('utf-8')
        print(out, err)
        self.assertTrue(out)

        # We create a file /etc/file1 before running rpm-ostree upgrade.
        # This file should persist, even in rolling back the upgrade.
        # This we assert in
        # TestAtomicRollbackPostReboot.test_atomic_rollback_post_reboot
        out, err, eid = system(
            'sudo cat /ostree/repo/refs/heads/ostree/0/1/0 > /etc/file1')
        err = err.decode('utf-8')
        print(out, err)
        self.assertFalse(err)
        out, err, eid = system('sudo atomic host upgrade')
        err = err.decode('utf-8')
        # Assert successful run
        print(out, err)
        self.assertFalse(err)
        time.sleep(30)


@unittest.skipUnless(if_atomic(), "It's not an Atomic image")
class TestAtomicUpgradePostReboot(unittest.TestCase):

    def test_upgrade_post_reboot(self):
        out, err, eid = system(
            'docker run --rm busybox true && echo "PASS"')
        out = out.decode('utf-8')
        self.assertEqual('PASS\n', out)


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
        print(out, err)

        out, err, eid = system('sudo atomic host rollback')
        err = err.decode('utf-8')
        self.assertFalse(err)
        print(out, err)
        time.sleep(30)


@unittest.skipUnless(if_atomic(), "It's not an Atomic image")
class TestAtomicRollbackPostReboot(unittest.TestCase):

    def test_atomic_rollback_post_reboot(self):
        out, err, eid = system('atomic host status')
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
        out, err, eid = system('sudo docker pull fedora:latest')
        self.assertFalse(err)
        time.sleep(10)
        out, err, eid = system(
            'sudo docker run --rm fedora:latest '
            'true && echo "PASS" || echo "FAIL"')
        out = out.decode('utf-8')
        self.assertEqual(out, 'PASS\n')

@unittest.skipUnless(if_atomic(), "It's not an Atomic image")
class TestAtomicCommand(unittest.TestCase):

    def test_atomic_command(self):
        out, err, eid = system('atomic run busybox')
        self.assertEqual(eid, 0, out+err)

# https://github.com/kushaldas/tunirtests/issues/8
@unittest.skipUnless(if_atomic(), "It's not an Atomic image")
class TestRootMount(unittest.TestCase):

    def test_root_mount(self):
        out, err, eid = system('docker run --rm -v /:/host busybox')
        self.assertEqual(eid, 0, out+err)

# https://github.com/kushaldas/tunirtests/issues/17
@unittest.skipUnless(if_atomic(), "It's not an Atomic image")
class Testreadonlymount(unittest.TestCase):

    def test_read_only(self):
        "Tests the read only dirs."
        dirs = [ '/bin/','/sbin/', '/usr/']
        for d in dirs:
            with self.assertRaises(OSError):
                with open(os.path.join(d, 'hooha.txt'), 'w') as fobj:
                    fobj.write('hello.')

# https://github.com/kushaldas/tunirtests/issues/17
@unittest.skipUnless(if_atomic(), "It's not an Atomic image")
class TestDockerDaemon(unittest.TestCase):

    def test_docker(self):
        out, err, eid = system('docker run --rm  --privileged -v /run:/run -v /:/host --net=host --entrypoint=/bin/bash fedora:23 -c "chroot /host/ docker version"')
        self.assertEqual(eid, 0, out+err)
        out = out.decode('utf-8')
        self.assertIn('Server version', out)

if __name__ == '__main__':
    unittest.main()
