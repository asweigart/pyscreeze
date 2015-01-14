import unittest
import sys
import os
import random

from PIL import Image
sys.path.insert(0, os.path.abspath('..'))
import pyscreeze

runningOnPython2 = sys.version_info[0] == 2


TEMP_FILENAME = '_delete_me.png'


# Helper functions to get current screen resolution on Windows, Mac OS X, or Linux.
# Non-Windows platforms require additional modules:
#   OS X: sudo pip3 install pyobjc-core
#         sudo pip3 install pyobjc
#   Linux: sudo pip3 install python3-Xlib
def resolutionOSX():
    return Quartz.CGDisplayPixelsWide(0), Quartz.CGDisplayPixelsHigh(0)

def resolutionX11():
    return _display.screen().width_in_pixels, _display.screen().height_in_pixels

def resolutionWin32():
    return (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))

# Assign the resolution() function to the function appropriate for the platform.
if sys.platform.startswith('java'):
    raise NotImplementedError('Jython is not yet supported by PyScreeze.')
elif sys.platform == 'darwin':
    import Quartz
    resolution = resolutionOSX
elif sys.platform == 'win32':
    import ctypes
    resolution = resolutionWin32
else:
    from Xlib.display import Display
    _display = Display(None)
    resolution = resolutionX11


# PNG file format magic numbers are 89 50 4E 47 0d 0a 1a 0a
pngMagicNumbers = [137, 80, 78, 71, 13, 10, 26, 10]
def isPng(filename):
    fp = open(filename, 'rb')
    fileMagicNumbers = fp.read(len(pngMagicNumbers))
    fp.close()
    if runningOnPython2:
        return fileMagicNumbers == bytearray(pngMagicNumbers)
    else:
        return fileMagicNumbers == bytes(pngMagicNumbers)


# JPG file format magic numbres are FF D8 FF
jpgMagicNumbers = [255, 216, 255]
def isJpg(filename):
    fp = open(filename, 'rb')
    fileMagicNumbers = fp.read(len(jpgMagicNumbers))
    fp.close()
    if runningOnPython2:
        return fileMagicNumbers == bytearray(jpgMagicNumbers)
    else:
        return fileMagicNumbers == bytes(jpgMagicNumbers)


class TestMagicNumbers(unittest.TestCase):
    def test_pngMagicNumbers(self):
        # Testing my test helper function to make sure it correctly
        # identifies PNG files.
        self.assertTrue(isPng('largenoise.png'))
        self.assertTrue(isPng('colornoise.png'))
        self.assertTrue(isPng('haystack1.png'))
        self.assertTrue(isPng('haystack2.png'))
        self.assertTrue(isPng('slash.png'))
        self.assertTrue(isPng('zophie.png'))
        self.assertTrue(isPng('zophie_face.png'))
        self.assertFalse(isPng('zophie.jpg'))
        self.assertFalse(isPng(__file__))

    def test_jpgMagicNumbers(self):
        # Testing my test helper function to make sure it correctly
        # identifies JPG files.
        self.assertFalse(isJpg('largenoise.png'))
        self.assertFalse(isJpg('colornoise.png'))
        self.assertFalse(isJpg('haystack1.png'))
        self.assertFalse(isJpg('haystack2.png'))
        self.assertFalse(isJpg('slash.png'))
        self.assertFalse(isJpg('zophie.png'))
        self.assertFalse(isJpg('zophie_face.png'))
        self.assertTrue(isJpg('zophie.jpg'))
        self.assertFalse(isJpg(__file__))

class TestGeneral(unittest.TestCase):
    def test_namesDefined(self):
        pyscreeze.locateAll
        pyscreeze.locate
        pyscreeze.locateOnScreen
        pyscreeze.locateAllOnScreen
        pyscreeze.locateCenterOnScreen
        pyscreeze.center
        pyscreeze.pixelMatchesColor
        pyscreeze.pixel
        pyscreeze.grab


    def test_screenshot(self):
        im = pyscreeze.screenshot(TEMP_FILENAME)
        self.assertTrue(isPng(TEMP_FILENAME))
        self.assertEqual(im.size, resolution())
        os.unlink(TEMP_FILENAME)


    def test_screenshot_regions(self):
        im = pyscreeze.screenshot(TEMP_FILENAME, region=(0, 0, 100, 150))
        self.assertEqual(im.size, (100, 150))
        os.unlink(TEMP_FILENAME)

        im = pyscreeze.screenshot(TEMP_FILENAME, region=(50, 50, 100, 150))
        self.assertEqual(im.size, (100, 150))
        os.unlink(TEMP_FILENAME)


    # TODO - lots of warnings about unclosed file handles for these tests.
    def test_locate_filename(self):
        self.assertEqual((94, 94, 4, 4), tuple(pyscreeze.locate('slash.png', 'haystack1.png')))
        self.assertEqual((93, 93, 4, 4), tuple(pyscreeze.locate('slash.png', 'haystack2.png')))

        self.assertEqual((94, 94, 4, 4), tuple(pyscreeze.locate('slash.png', 'haystack1.png', grayscale=True)))
        self.assertEqual((93, 93, 4, 4), tuple(pyscreeze.locate('slash.png', 'haystack2.png', grayscale=True)))

        self.assertEqual(None, pyscreeze.locate('slash.png', 'colornoise.png'))
        self.assertEqual(None, pyscreeze.locate('slash.png', 'colornoise.png', grayscale=True))


    def test_locate_im(self):
        slashFp = open('slash.png' ,'rb')
        haystack1Fp = open('haystack1.png' ,'rb')
        haystack2Fp = open('haystack2.png' ,'rb')
        colorNoiseFp = open('colornoise.png' ,'rb')
        slashIm = Image.open(slashFp)
        haystack1Im = Image.open(haystack1Fp)
        haystack2Im = Image.open(haystack2Fp)
        colorNoiseIm = Image.open(colorNoiseFp)

        self.assertEqual((94, 94, 4, 4), tuple(pyscreeze.locate(slashIm, haystack1Im)))
        self.assertEqual((93, 93, 4, 4), tuple(pyscreeze.locate(slashIm, haystack2Im)))

        self.assertEqual((94, 94, 4, 4), tuple(pyscreeze.locate(slashIm, haystack1Im, grayscale=True)))
        self.assertEqual((93, 93, 4, 4), tuple(pyscreeze.locate(slashIm, haystack2Im, grayscale=True)))

        self.assertEqual(None, pyscreeze.locate(slashIm, colorNoiseIm))
        self.assertEqual(None, pyscreeze.locate(slashIm, colorNoiseIm, grayscale=True))

        slashFp.close()
        haystack1Fp.close()
        haystack2Fp.close()
        colorNoiseFp.close()

    def test_locateAll_filename(self):
        self.assertEqual(((94, 94, 4, 4),), tuple(pyscreeze.locateAll('slash.png', 'haystack1.png')))
        self.assertEqual(((93, 93, 4, 4), (94, 94, 4, 4), (95, 95, 4, 4)), tuple(pyscreeze.locateAll('slash.png', 'haystack2.png')))

        self.assertEqual(((94, 94, 4, 4),), tuple(pyscreeze.locateAll('slash.png', 'haystack1.png', grayscale=True)))
        self.assertEqual(((93, 93, 4, 4), (94, 94, 4, 4), (95, 95, 4, 4)), tuple(pyscreeze.locateAll('slash.png', 'haystack2.png', grayscale=True)))

        self.assertEqual((), tuple(pyscreeze.locateAll('slash.png', 'colornoise.png')))
        self.assertEqual((), tuple(pyscreeze.locateAll('slash.png', 'colornoise.png', grayscale=True)))

    def test_locateAll_im(self):
        slashFp = open('slash.png' ,'rb')
        haystack1Fp = open('haystack1.png' ,'rb')
        haystack2Fp = open('haystack2.png' ,'rb')
        colorNoiseFp = open('colornoise.png' ,'rb')
        slashIm = Image.open(slashFp)
        haystack1Im = Image.open(haystack1Fp)
        haystack2Im = Image.open(haystack2Fp)
        colorNoiseIm = Image.open(colorNoiseFp)

        self.assertEqual(((94, 94, 4, 4),), tuple(pyscreeze.locateAll(slashIm, haystack1Im)))
        self.assertEqual(((93, 93, 4, 4), (94, 94, 4, 4), (95, 95, 4, 4)), tuple(pyscreeze.locateAll(slashIm, haystack2Im)))

        self.assertEqual(((94, 94, 4, 4),), tuple(pyscreeze.locateAll(slashIm, haystack1Im, grayscale=True)))
        self.assertEqual(((93, 93, 4, 4), (94, 94, 4, 4), (95, 95, 4, 4)), tuple(pyscreeze.locateAll(slashIm, haystack2Im, grayscale=True)))

        self.assertEqual((), tuple(pyscreeze.locateAll(slashIm, colorNoiseIm)))
        self.assertEqual((), tuple(pyscreeze.locateAll(slashIm, colorNoiseIm, grayscale=True)))

        slashFp.close()
        haystack1Fp.close()
        haystack2Fp.close()
        colorNoiseFp.close()

    def test_imageNotFound(self):
        colorNoiseFp = open('colornoise.png' ,'rb')
        colorNoiseIm = Image.open(colorNoiseFp)
        slashFp = open('slash.png' ,'rb')
        slashIm = Image.open(slashFp)

        oldSetting = pyscreeze.RAISE_IF_NOT_FOUND

        pyscreeze.RAISE_IF_NOT_FOUND = True
        self.assertRaises(pyscreeze.ImageNotFoundException, pyscreeze.locate, slashIm, colorNoiseIm)
        pyscreeze.RAISE_IF_NOT_FOUND = False
        self.assertEqual(None, pyscreeze.locate(slashIm, colorNoiseIm))

        pyscreeze.RAISE_IF_NOT_FOUND = oldSetting
        colorNoiseFp.close()
        slashFp.close()

    def test_center(self):
        self.assertEqual((10, 10), pyscreeze.center((0, 0, 20, 20)))
        self.assertEqual((10, 10), pyscreeze.center((5, 5, 10, 10)))

        self.assertEqual((100, 100), pyscreeze.center((0, 0, 200, 200)))
        self.assertEqual((100, 100), pyscreeze.center((50, 50, 100, 100)))

    def test_locate_im_step(self):
        slashFp = open('slash.png' ,'rb')
        haystack1Fp = open('haystack1.png' ,'rb')
        haystack2Fp = open('haystack2.png' ,'rb')
        colorNoiseFp = open('colornoise.png' ,'rb')
        slashIm = Image.open(slashFp)
        haystack1Im = Image.open(haystack1Fp)
        haystack2Im = Image.open(haystack2Fp)
        colorNoiseIm = Image.open(colorNoiseFp)

        for step in range(1, 10):
            self.assertEqual(((94, 94, 4, 4), step), (tuple(pyscreeze.locate(slashIm, haystack1Im, step=step)), step))
            self.assertEqual(((93, 93, 4, 4), step), (tuple(pyscreeze.locate(slashIm, haystack2Im, step=step)), step))

            self.assertEqual(((94, 94, 4, 4), step), (tuple(pyscreeze.locate(slashIm, haystack1Im, grayscale=True, step=step)), step))
            self.assertEqual(((93, 93, 4, 4), step), (tuple(pyscreeze.locate(slashIm, haystack2Im, grayscale=True, step=step)), step))

            self.assertEqual((None, step), (pyscreeze.locate(slashIm, colorNoiseIm, step=step), step))
            self.assertEqual((None, step), (pyscreeze.locate(slashIm, colorNoiseIm, grayscale=True, step=step), step))

        slashFp.close()
        haystack1Fp.close()
        haystack2Fp.close()
        colorNoiseFp.close()


if __name__ == '__main__':
    unittest.main()
