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


class TunirNonGatingtestsCpio(unittest.TestCase):

    def setUp(self):
        """Recording the current working directory"""
        self.current_working_directory = os.getcwd()

    def test_cpio(self):
        """Tests to check basic cpio functions"""

        outdir = '/var/tmp/cpio/cpio_out'
        indir = '/var/tmp/cpio/cpio_in'
        passdir = '/var/tmp/cpio/cpio_pass'

        if os.path.exists('/var/tmp/cpio'):
            system('rm -rf /var/tmp/cpio')

        system('mkdir -p %s' % outdir)
        system('mkdir -p %s' % indir)
        system('mkdir -p %s' % passdir)

        # Basic copy out test
        out, err, eid = system('ls | cpio -o > %s/cpio.out' % outdir)
        out = out.decode('utf-8')
        err = err.decode('utf-8')
        self.assertEqual(eid, 0, out+err)

        # Basic copy in test
        os.chdir(indir)
        out, err, eid = system('cpio -i < %s/cpio.out' % outdir)
        out = out.decode('utf-8')
        err = err.decode('utf-8')
        self.assertEqual(eid, 0, out+err)

        # Basic pass through test
        os.chdir(indir)
        out, err, eid = system('find . | cpio -pd %s' % passdir)
        out = out.decode('utf-8')
        err = err.decode('utf-8')
        self.assertEqual(eid, 0, out+err)

        # Check that the working directories are the same
        out, err, eid = system('diff %s %s &>/dev/null' % (passdir, indir))
        out = out.decode('utf-8')
        err = err.decode('utf-8')
        self.assertEqual(eid, 0, out+err)

    def tearDown(self):
        """Returning to present directory"""
        os.chdir(self.current_working_directory)


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

class TunirNonGatingtestfile(unittest.TestCase):

    def test_file(self):
        """file test"""

        pngfile = '/usr/share/anaconda/boot/syslinux-splash.png'
        testfilepath = '/tmp/p_file_link_test'

        #Checks if file package is installed
        out, err, eid = system('rpm -q file')
        out = out.decode('utf-8')
        err = err.decode('utf-8')
        self.assertEqual(eid, 0, out+err)

        #Checks if file can recognize mime executable type
        out, err, eid = system('file /bin/bash -i')
        out = out.decode('utf-8')
        self.assertIn('application/x-sharedlib', out, out)

        #Checks if file can recognize image mime file type
        out, err, eid = system('file %s -i' % pngfile)
        out = out.decode('utf-8')
        self.assertIn('image/png', out, out)

        #Checks if file can recognize symlink mime file type
        out, err, eid = system('ln -s /etc/hosts %s' % testfilepath)
        out = out.decode('utf-8')
        err = err.decode('utf-8')
        self.assertEqual(eid, 0, out+err)

        out, err, eid = system('file -i %s' % testfilepath)
        out = out.decode('utf-8')
        self.assertIn('inode/symlink', out, out)

    def tearDown(self):
        """Deletes the symlink created for test"""
        os.remove('/tmp/p_file_link_test')

class TunirNonGatingtestcurl(unittest.TestCase):

    def test_curl(self):
        """Tests that curl can access http-host and retrieve index.html"""

        URL = "http://fedoraproject.org"

        #Querying url
        out, err, eid = system('curl --location -s %s' % URL)
        out = out.decode('utf-8')
        self.assertIn('Fedora', out)

if __name__ == '__main__':
    unittest.main()
