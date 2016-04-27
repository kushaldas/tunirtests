"""
This test is to check restorecon command for selinux context
"""

import unittest
from .testutils import system


class TestSELinux(unittest.TestCase):
    """
    selinux_test class
    """
    def test_selinux(self):
        """
        actual test case
        """
        out, err, retcode = system("ls -lZ /etc/machine-id")
        out = out.decode('utf-8')
        system("restorecon -v /etc/machine-id")
        out2, err2, retcode2 = system("ls -lZ /etc/machine-id")
        out2 = out2.decode('utf-8')
        self.assertEqual(out, out2)


if __name__ == '__main__':
    unittest.main()
