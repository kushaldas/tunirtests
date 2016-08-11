import unittest
from .testutils import system


class TestUmountRoot(unittest.TestCase):

    """
    This test is to check if user can
    unmount the "/" partition in fedora
    """

    def test_umountroot(self):
        out, err, retcode = system("umount /")
        out = out.decode('utf-8')
        self.assertNotEqual(retcode, 0)

if __name__ == '__main__':
    unittest.main()
