import unittest
import re
from testutils import system, if_atomic


@unittest.skipUnless(if_atomic(), "It's not an Atomic image")
class TestDockerStorageSetup(unittest.TestCase):

    def test_journalctl_logs(self):
        """Test journalctl logs for docker-storage-setup"""
        out, err, eid = system(
            'journalctl -o cat --unit docker-storage-setup.service'
        )
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
        self.assertTrue(
            re.search(r'atomicos-root.*\d+(?:.\d+)?G.*lvm.*/sysroot.*\n', out)
        )
        self.assertTrue(
            re.search(r'atomicos-docker--meta.*\d+(?:.\d+)?M.*lvm', out)
        )
        self.assertTrue(
            re.search(r'atomicos-docker--data.*\d+(?:.\d+)?G.*lvm', out)
        )


if __name__ == '__main__':
    unittest.main()
