import unittest
from .testutils import system

class TestReboot(unittest.TestCase):
    def test_lastreboot(self):
        """Checks for system reboot."""
        out, err, retcode = system("last reboot | head -1")
        out = out.decode('utf-8')
        self.assertEqual(retcode, 0, out)
        self.assertIn('system', out)

if __name__ == '__main__':
    unittest.main()
