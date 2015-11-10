import unittest
import re
from .testutils import system
    
class TunirNonGatingtests(unittest.TestCase):
    
    def test_bash(self):
        """Tests the bash version as the same of upstream"""
        out, err, eid = system('bash --version')
        out = out.decode('utf-8')
        self.assertIn("-redhat-linux-gnu", out, out)

if __name__ == '__main__':
    unittest.main()
