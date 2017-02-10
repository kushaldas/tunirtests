import unittest
from .testutils import system, if_vagrant


@unittest.skipUnless(if_vagrant(), "It's not a Vagrant image")
class TestVagrantSwitchUser(unittest.TestCase):
    """Switch User Test for Vagrant based images"""

    def setUp(self):
        "Add a new user"
        system('sudo useradd testuser')

    def test_vagrant_switch_user(self):
        "Test for switching user in vagrant Box"
        out, err, eid = system("sudo su testuser")
        out = out.decode('utf-8')
        err = err.decode('utf-8')
        self.assertEqual(eid, 0, out+err)

    def tearDown(self):
        "Delete the user created"
        system("sudo userdel testuser")


if __name__ == '__main__':
    unittest.main()
