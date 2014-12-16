import random, sys, os, time, cProfile, pstats, pprint

from PIL import Image
sys.path.insert(0, os.path.abspath('..'))
import pyscreeze

pyscreeze.RAISE_IF_NOT_FOUND = True

def locateTest():
    largeNoiseFp = open('largenoise.png' ,'rb')
    largeNoiseIm = Image.open(largeNoiseFp)

    imageWidth, imageHeight = largeNoiseIm.size
    bottomRightCorner100x100 = largeNoiseIm.crop((imageWidth - 100, imageHeight - 100, imageWidth, imageHeight))

    for step in (1, 2, 4, 8, 16, 32):
        startTime = time.time()
        result = pyscreeze.locate(bottomRightCorner100x100, largeNoiseIm, step=step)
        print('bottomRightCorner100x100 (step %s) located at %s in: %s seconds' % (step, result, round(time.time() - startTime, 2)))

    largeNoiseFp.close()

def largegrayscaleTest():
    largeNoiseFp = open('largenoise.png' ,'rb')
    largeNoiseIm = Image.open(largeNoiseFp)

    imageWidth, imageHeight = largeNoiseIm.size
    bottomRightCorner100x100 = largeNoiseIm.crop((imageWidth - 100, imageHeight - 100, imageWidth, imageHeight))

    startTime = time.time()
    result = pyscreeze.locate(bottomRightCorner100x100, largeNoiseIm, grayscale=False)
    print('Non-grayscale located at %s in: %s seconds' % (result, round(time.time() - startTime, 2)))

    startTime = time.time()
    result = pyscreeze.locate(bottomRightCorner100x100, largeNoiseIm, grayscale=True)
    print('Grayscale located at %s in: %s seconds' % (result, round(time.time() - startTime, 2)))

    largeNoiseFp.close()


def smallgrayscaleTest():
    largeNoiseFp = open('largenoise.png' ,'rb')
    largeNoiseIm = Image.open(largeNoiseFp)

    imageWidth, imageHeight = largeNoiseIm.size
    bottomRightCorner30x30 = largeNoiseIm.crop((imageWidth - 30, imageHeight - 30, imageWidth, imageHeight))
    largeNoiseIm = largeNoiseIm.crop((imageWidth - 100, imageHeight - 100, imageWidth, imageHeight))

    startTime = time.time()
    result = pyscreeze.locate(bottomRightCorner30x30, largeNoiseIm, grayscale=False)
    print('Non-grayscale located at %s in: %s seconds' % (result, round(time.time() - startTime, 2)))

    startTime = time.time()
    result = pyscreeze.locate(bottomRightCorner30x30, largeNoiseIm, grayscale=True)
    print('Grayscale located at %s in: %s seconds' % (result, round(time.time() - startTime, 2)))

    largeNoiseFp.close()


def smallNeedleVsLargeNeedle():
    # This test shows that larger needle images take longer to find. However, for small-ish needles (100x100 and smaller) it doesn't really matter.
    largeNoiseFp = open('largenoise.png' ,'rb')
    largeNoiseIm = Image.open(largeNoiseFp)

    imageWidth, imageHeight = largeNoiseIm.size
    needle10x10   = largeNoiseIm.crop((imageWidth - 10,  imageHeight - 10,  imageWidth, imageHeight))
    needle100x100 = largeNoiseIm.crop((imageWidth - 100, imageHeight - 100, imageWidth, imageHeight))
    needle500x500 = largeNoiseIm.crop((imageWidth - 500, imageHeight - 500, imageWidth, imageHeight))

    profiler = cProfile.Profile()
    profiler.enable()
    list(pyscreeze.locateAll(needle10x10, largeNoiseIm))
    profiler.disable()
    print('10x10 needle:')
    pstats.Stats(profiler).sort_stats('cumulative').print_stats(1)

    profiler = cProfile.Profile()
    profiler.enable()
    list(pyscreeze.locateAll(needle100x100, largeNoiseIm))
    profiler.disable()
    print('100x100 needle:')
    pstats.Stats(profiler).sort_stats('cumulative').print_stats(1)

    profiler = cProfile.Profile()
    profiler.enable()
    list(pyscreeze.locateAll(needle500x500, largeNoiseIm))
    profiler.disable()
    print('500x500 needle:')
    pstats.Stats(profiler).sort_stats('cumulative').print_stats(1)



#largegrayscaleTest()
smallgrayscaleTest()