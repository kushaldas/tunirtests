import unittest
from .testutils import system

class sshkeygenTest(unittest.TestCase):
    def test_sshkeygen(self):
        """This is a test case for ssh-keygen command."""        
        system('ssh-keygen -t rsa -f ~/.ssh/id_rsa -q -P ""')
        out, err ,retcode = system('cat ~/.ssh/id_rsa.pub')
        out = out.decode('utf-8')
        self.assertIn('ssh-rsa',out)
if __name__== '__main__':
     unittest.main()
