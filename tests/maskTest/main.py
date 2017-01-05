import pyscreeze
from PIL import Image

def _printResult(result):
	print("result = %s" % (str(result)))
	print("len = %s" % (len(result)))

def doTest(testName, expected, needleImageName, haystackImageName, maskImageName, maskChannel):
	with open(needleImageName, 'rb') as f:
		needleImgObj = Image.open(needleImageName)
	with open(haystackImageName, 'rb') as f:
		haystackImgObj = Image.open(haystackImageName)

	if maskImageName:
		with open(maskImageName, 'rb') as f:
			maskImgObj = Image.open(maskImageName)

	results = [
		("img names", tuple(pyscreeze.locateAll(needleImageName, haystackImageName, maskImage=maskImageName, maskChannel=maskChannel))),
		("img objects", tuple(pyscreeze.locateAll(needleImgObj, haystackImgObj, maskImage=maskImageName, maskChannel=maskChannel))),
		("grayscale", tuple(pyscreeze.locateAll(needleImgObj, haystackImgObj, grayscale=True, maskImage=maskImageName, maskChannel=maskChannel))),
	]

	if needleImageName == maskImageName:
		results += [
			("needle == mask", tuple(pyscreeze.locateAll(needleImgObj, haystackImgObj, maskImage=needleImgObj, maskChannel=maskChannel))),
		]

	passed = True
	for desc, result in results:
		if result != expected:
			print("Fail: %s %s" % (testName, desc))
			passed = False

	if passed:
		print("%s passed" % (testName))

def runTests():
	# result = tuple(pyscreeze.locateAll("crossRGB.png", "search2.png", maskImage="crossMaskBlack.png", maskChannel=0))
	# _printResult(result)

	expected = tuple()
	doTest("blank mask", expected, "crossRGB.png", "search2.png", "crossMaskBlack.png", None)

	expected = ((13, 5, 5, 5), (25, 5, 5, 5), (13, 9, 5, 5), (16, 22, 5, 5))
	doTest("cross maskImg", expected, "crossRGB.png", "search2.png", "crossRGB.png", None)
	doTest("cross maskR", expected, "crossRGB.png", "search2.png", None, 0)

	expected = ((-8, -10, 127, 128), (199, 205, 127, 128), (56, 278, 127, 128), (222, 336, 127, 128))
	doTest("smile maskImgR", expected, "smileRGB.png", "search.png", "mask.png", None)
	doTest("smile maskA", expected, "smileRGBA.png", "search.png", None, 3)

	expected = ((-8, -10, 127, 128), (318, 54, 127, 128), (74, 76, 127, 128), (199, 205, 127, 128), (56, 278, 127, 128), (222, 336, 127, 128), (3, 382, 127, 128), (4, 382, 127, 128), (5, 382, 127, 128), (402, 398, 127, 128))
	doTest("smile maskImgG", expected, "smileRGB.png", "search.png", "mask.png", 1)

if __name__ == "__main__":
	runTests()
