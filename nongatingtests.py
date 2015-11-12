import unittest
import re
import os
from .testutils import system

class TunirNonGatingtests(unittest.TestCase):

    def test_bash(self):
        """Tests the bash version as the same of upstream"""
        out, err, eid = system('bash --version')
        out = out.decode('utf-8')
        self.assertIn("-redhat-linux-gnu", out, out)

class TunirNonGatingtestBzip2(unittest.TestCase):

    def setUp(self):
        """Creates a file for bzip2 testing"""
        with open('/var/tmp/bzip2-test.txt', 'w') as FILE:
            FILE.write('bzip2-test of single file')

    def test_bzip2(self):
        """Test to run a file through bzip2,bzcat,bunzip2"""

        testfile = '/var/tmp/bzip2-test.txt'
        testbz2file = '/var/tmp/bzip2-test.txt.bz2'

        #Runs a file through bzip2
        out, err, eid = system('bzip2 %s' % testfile)
        out = out.decode('utf-8')
        err = err.decode('utf-8')
        self.assertEqual(eid, 0, out+err)

        #Runs a file through bzcat
        out, err, eid = system("bzcat %s | grep -q 'bzip2-test of single file'" % testbz2file)
        out = out.decode('utf-8')
        err = err.decode('utf-8')
        self.assertEqual(eid, 0, out+err)

        #Runs a file through bunzip2
        out, err, eid = system("bunzip2 %s" % testbz2file)
        out = out.decode('utf-8')
        err = err.decode('utf-8')
        self.assertEqual(eid, 0, out+err)

        #Checks the file contents
        out, err, eid = system("grep -q 'bzip2-test of single file' %s" % testfile)
        out = out.decode('utf-8')
        err = err.decode('utf-8')
        self.assertEqual(eid, 0, out+err)

        #Checks if the bz2 file exists
        self.assertFalse(os.path.exists(testbz2file))

    def tearDown(self):
        """Deletes the file created for bzip2 testing"""
        os.remove('/var/tmp/bzip2-test.txt')

if __name__ == '__main__':
    unittest.main()