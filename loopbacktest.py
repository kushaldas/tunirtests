import unittest
from .testutils import system

class Loopbacktest(unittest.TestCase):
    def test_loopback(self):
        out,err,retcode = system("dd if=/dev/zero of=/opt/virtualfs bs=1MiB count=10")
        self.assertEqual(retcode, 0, msg=err)
        out,err,retcode = system("losetup /dev/loop996 /opt/virtualfs")
        self.assertEqual(retcode, 0 , msg=err)
        out, err,retcode = system("mkfs.ext4 -m 1 -v /dev/loop996")
        self.assertEqual(retcode, 0, msg=err)
        out,err,retcode = system("mkdir /mnt/vfs")
        self.assertEqual(retcode, 0, msg=err)
        out,err,retcode = system("mount -t ext4 /dev/loop996 /mnt/vfs/")
        self.assertEqual(retcode, 0 ,msg=err)
        out,err,retcode = system("touch /mnt/vfs/hello.txt")
        self.assertEqual(retcode, 0 ,msg=err)
        out,err,retcode = system("umount /mnt/vfs")
        self.assertEqual(retcode, 0 ,msg=err)
        out,err,retcode = system("losetup -d /dev/loop996")
        self.assertEqual(retcode, 0 ,msg=err)
        out,err,retcode = system(" losetup /dev/loop996 /opt/virtualfs")
        self.assertEqual(retcode, 0 ,msg=err)
        out,err,retcode = system("mount -t ext4 /dev/loop996 /mnt/vfs/")
        self.assertEqual(retcode, 0 ,msg=err)
        out,err,retcode = system("ls /mnt/vfs/")
        out = out.decode('utf-8')
        self.assertIn('hello.txt',out ,msg=err)
        out,err,retcode = system("losetup -d /dev/loop996")
        self.assertEqual(retcode, 0 ,msg=err)


if __name__ == '__main__':
    unittest.main()
