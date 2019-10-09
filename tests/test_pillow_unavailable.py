# This unit test will test PyScreeze in a condition where PIL is unavailable.
# The locate and screenshot functions that require Pillow should fail under
# this circumstance. This test checks to make sure those failures happen.

# NOTE: This is in a separate .py file because we need to ensure that
# the real PIL module isn't imported, and there's no convenient way to
# "unimport" modules in Python after they've been imported.

# NOTE: PIL and Pillow mean the same thing in this document.

import os
import sys
import unittest

scriptFolder = os.path.dirname(os.path.realpath(__file__))
os.chdir(scriptFolder)

sys.path.insert(0, scriptFolder) # Ensure that we import our fake PIL.py even if Pillow is actually installed.

class TestPillowNotImported(unittest.TestCase):

    def test_functionsThatRequirePillow(self):
        try:
            import cv2, numpy
            opencvNotInstalled = False
        except ImportError:
            opencvNotInstalled = True

        if (sys.platform == 'win32') and (opencvNotInstalled):
            with self.assertRaises(pyscreeze.PyScreezeException):
                #import pdb;pdb.set_trace()
                pyscreeze.screenshot('foo.png')

            with self.assertRaises(pyscreeze.PyScreezeException):
                pyscreeze.locateOnScreen('foo.png')

            with self.assertRaises(pyscreeze.PyScreezeException):
                pyscreeze.locateAllOnScreen('foo.png')

            with self.assertRaises(pyscreeze.PyScreezeException):
                pyscreeze.locateAll('foo.png', 'foo.png')
        else:
            pass # TODO - add some kind of warning here that we aren't actually testing anything, maybe?

if __name__ == '__main__':
    # Ensure that our fake PIL module is imported, which simulates PIL not being available for importing.
    fileObj = open('PIL.py', 'w')
    fileObj.write("""raise ImportError('fake import error')\n""")
    fileObj.close()

    import pyscreeze # Import pyscreeze and fool it into thinking PIL is unavailable.

    try:
        os.unlink('PIL.py') # Delete the fake PIL.py file so that other tests use the real PIL module.
    except Exception():
        pass

    unittest.main()
