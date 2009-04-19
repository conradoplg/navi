from appcommon.model import shortcut
import unittest
import mox


class Test(unittest.TestCase):


    def test_shortcut(self):
        FLAGS = 1
        KEYCODE = 2
        NAME = 'Name'
        
        s1 = shortcut.Shortcut(FLAGS, KEYCODE)
        s2 = shortcut.Shortcut(FLAGS, KEYCODE)
        s3 = shortcut.Shortcut(FLAGS+1, KEYCODE)
        s4 = shortcut.Shortcut(FLAGS, KEYCODE+1)
        s5 = shortcut.Shortcut(FLAGS+1, KEYCODE+1)
        
        self.assertEquals(s1, s2)
        self.assertNotEquals(s1, s3)
        self.assertNotEquals(s1, s4)
        self.assertNotEquals(s1, s5)
        self.assertTrue(s1 != s3)
        
        old = shortcut.GetAcceleratorName
        fn = shortcut.GetAcceleratorName = mox.MockAnything()
        fn((FLAGS, KEYCODE)).AndReturn(NAME)
        mox.Replay(fn)
        self.assertEquals(NAME, s1.name)
        mox.Verify(fn)
        shortcut.GetAcceleratorName = old

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_shortcut']
    unittest.main()