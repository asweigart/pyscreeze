import unittest
import sys
import os
import pyscreeze

scriptFolder = os.path.dirname(os.path.realpath(__file__))
# Delete PIL.py, which is made by test_pillow_unavailable.py, just in case it
# was left over from some incomplete run of that test.
if os.path.exists(os.path.join(scriptFolder, 'PIL.py')):
    os.unlink(os.path.join(scriptFolder, 'PIL.py'))

from PIL import Image


# Change the cwd to this file's folder, because that's where the test image files are located.
scriptFolder = os.path.dirname(os.path.realpath(__file__))
os.chdir(scriptFolder)

RUNNING_ON_PYTHON_2 = sys.version_info[0] == 2
TEMP_FILENAME = '_delete_me.png'

# On Linux, figure out which window system is being used.
if sys.platform.startswith('linux'):
    RUNNING_X11 = False
    RUNNING_WAYLAND = False
    if os.environ.get('XDG_SESSION_TYPE') == 'x11':
        RUNNING_X11 = True
        RUNNING_WAYLAND = False
    elif os.environ.get('XDG_SESSION_TYPE') == 'wayland':
        RUNNING_WAYLAND = True
        RUNNING_X11 = False
    elif 'WAYLAND_DISPLAY' in os.environ:
        RUNNING_WAYLAND = True
        RUNNING_X11 = False

# Helper functions to get current screen resolution on Windows, Mac OS X, or Linux.
# Non-Windows platforms require additional modules:
#   OS X: sudo pip3 install pyobjc-core
#         sudo pip3 install pyobjc
#   Linux: sudo pip3 install python3-Xlib
def resolutionOSX():
    return Quartz.CGDisplayPixelsWide(0), Quartz.CGDisplayPixelsHigh(0)

def resolutionX11():
    return _display.screen().width_in_pixels, _display.screen().height_in_pixels

def resolutionWayland():
    xrandrOutput = subprocess.run(['xrandr'], shell=True, capture_output=True, text=True).stdout
    mo = re.search(r'current (\d+) x (\d+)', xrandrOutput)
    if mo is None:
        raise Exception('xrandr output does not list the wayland resolution. xrandr output:\n' + xrandrOutput)
    return int(mo.group(1)), int(mo.group(2))

def resolutionWin32():
    return (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))

# Assign the resolution() function to the function appropriate for the platform.
if sys.platform == 'darwin':
    import Quartz
    resolution = resolutionOSX
elif sys.platform == 'win32':
    import ctypes
    resolution = resolutionWin32
elif sys.platform.startswith('linux'):
    if RUNNING_X11:
        from Xlib.display import Display
        _display = Display(None)
        resolution = resolutionX11
    elif RUNNING_WAYLAND:
        import subprocess
        import re
        resolution = resolutionWayland
else:
    assert False, 'PyScreeze is not supported on platform ' + sys.platform


# PNG file format magic numbers are 89 50 4E 47 0d 0a 1a 0a
pngMagicNumbers = [137, 80, 78, 71, 13, 10, 26, 10]
def isPng(filename):
    fp = open(filename, 'rb')
    fileMagicNumbers = fp.read(len(pngMagicNumbers))
    fp.close()
    if RUNNING_ON_PYTHON_2:
        return fileMagicNumbers == bytearray(pngMagicNumbers)
    else:
        return fileMagicNumbers == bytes(pngMagicNumbers)


# JPG file format magic numbres are FF D8 FF
jpgMagicNumbers = [255, 216, 255]
def isJpg(filename):
    fp = open(filename, 'rb')
    fileMagicNumbers = fp.read(len(jpgMagicNumbers))
    fp.close()
    if RUNNING_ON_PYTHON_2:
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


    def test_screenshot(self):
        im = pyscreeze.screenshot(TEMP_FILENAME)
        self.assertTrue(isPng(TEMP_FILENAME))
        self.assertEqual(im.size, resolution()) # TODO shouldn't this fail on Windows for multi-monitor setups?
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

        pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = True
        with self.assertRaises(pyscreeze.ImageNotFoundException):
            pyscreeze.locate('slash.png', 'colornoise.png')
        with self.assertRaises(pyscreeze.ImageNotFoundException):
            pyscreeze.locate('slash.png', 'colornoise.png', grayscale=True)

        pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = False
        self.assertEqual(pyscreeze.locate('slash.png', 'colornoise.png'), None)
        self.assertEqual(pyscreeze.locate('slash.png', 'colornoise.png', grayscale=True), None)

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

        pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = True
        with self.assertRaises(pyscreeze.ImageNotFoundException):
            pyscreeze.locate(slashIm, colorNoiseIm)
        with self.assertRaises(pyscreeze.ImageNotFoundException):
            pyscreeze.locate(slashIm, colorNoiseIm, grayscale=True)

        pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = False
        self.assertEqual(pyscreeze.locate(slashIm, colorNoiseIm), None)
        self.assertEqual(pyscreeze.locate(slashIm, colorNoiseIm, grayscale=True), None)

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

        pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = True
        with self.assertRaises(pyscreeze.ImageNotFoundException):
            pyscreeze.locate(slashIm, colorNoiseIm)

        pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = False
        self.assertEqual(pyscreeze.locate(slashIm, colorNoiseIm), None)

        colorNoiseFp.close()
        slashFp.close()

    def test_center(self):
        self.assertEqual((10, 10), pyscreeze.center((0, 0, 20, 20)))
        self.assertEqual((10, 10), pyscreeze.center((5, 5, 10, 10)))

        self.assertEqual((100, 100), pyscreeze.center((0, 0, 200, 200)))
        self.assertEqual((100, 100), pyscreeze.center((50, 50, 100, 100)))

    """
    # Disabling step test; we don't use this feature because it does not bring any significant performance improvement.
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
        """

class TestStressTest(unittest.TestCase):
    def test_1000screenshots(self):
        # This test takes about two minutes for 200 screenshots.
        # On Windows, if I change PyScreeze away from Pillow and make win32 api calls directly but forget to release
        # the DCs (display contexts), the program would fail after about 90 or screenshots.
        # https://stackoverflow.com/questions/3586046/fastest-way-to-take-a-screenshot-with-python-on-windows
        if sys.platform == 'win32':
            for i in range(200):
                pyscreeze.screenshot(TEMP_FILENAME)
                self.assertTrue(isPng(TEMP_FILENAME))
                os.unlink(TEMP_FILENAME)

if __name__ == '__main__':
    unittest.main()
