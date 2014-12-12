import random, sys, os, time

from PIL import Image
sys.path.insert(0, os.path.abspath('..'))
import pyscreeze

def locateTest():
    largeNoiseFp = open('largenoise.png' ,'rb')
    largeNoiseIm = Image.open(largeNoiseFp)

    imageWidth, imageHeight = largeNoiseIm.size
    bottomRightCorner100x100 = largeNoiseIm.crop((imageWidth - 100, imageHeight - 100, imageWidth , imageHeight ))

    for step in (1, 2, 4, 8, 16, 32):
        startTime = time.time()
        pyscreeze.locate(bottomRightCorner100x100, largeNoiseIm, step=step)
        print('bottomRightCorner100x100 (step %s) located in: %s seconds' % (step, round(time.time() - startTime, 2)))

    largeNoiseFp.close()

locateTest()