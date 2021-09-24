import cv2
import numpy as np

extensions = ['.png', '.jpg', '.jpeg']
def checkExtensions(fileName):
    for ext in extensions:
        if ext in fileName.lower():
            return True
    return False

def getGrayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# This function crops out the top user border,
# as well as the bottom factions choice. This makes
# it possible to stitch on a common hero location,
# this location is typically the bottom/top row of
# the corresponding images.

def cropImg(img):
    return img[220:img.shape[0]-600 :].copy()

def trimBlankSpace(frame):
    if not np.sum(frame[0]):
        return trimBlankSpace(frame[1:])
    if not np.sum(frame[-1]):
        return trimBlankSpace(frame[:-2])
    if not np.sum(frame[:,0]):
        return trimBlankSpace(frame[:,1:])
    if not np.sum(frame[:,-1]):
        return trimBlankSpace(frame[:,:-2])
    return frame

def floodFillBackground(img, seedPoints, d):

    cv2.floodFill(img, None, seedPoint=seedPoints[0], newVal=(0, 0, 0), loDiff=(d,d,d,d), upDiff=(d,d,d,d))
    cv2.floodFill(img, None, seedPoint=seedPoints[1], newVal=(0, 0, 0), loDiff=(d,d,d,d), upDiff=(d,d,d,d))

    return img

def stitchImages(imgTop, imgBottom, outputName, difference):
    img_ = cropImg(cv2.imread(imgTop))
    img = cropImg(cv2.imread(imgBottom))

    img1 = getGrayscale(img_.copy())
    img2 = getGrayscale(img.copy())

    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    match = cv2.BFMatcher()
    matches = match.knnMatch(des1,des2,k=2)

    good = []
    for m,n in matches:
        if .03*m.distance < 0.03*n.distance:
            good.append(m)
    
    # DEBUG TOOLS
    # draw_params = dict(matchColor=(0,255,0),
    #                       singlePointColor=None,
    #                       flags=2)
    #
    # img3 = cv2.drawMatches(img_,kp1,img,kp2,good,None,**draw_params)

    MIN_MATCH_COUNT = 10
    if len(good) > MIN_MATCH_COUNT:
        srcPts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,2,1)
        dstPts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,2,1)

        M, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5.0)

        h,w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts, M)

        # DEBUG TOOLS
        #img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

    else:
        print("Not enought matches are found - %d/%d", (len(good)/MIN_MATCH_COUNT))

    dst = cv2.warpPerspective(img_,M,(img.shape[1], img.shape[0]))

    trimmedDst= trimBlankSpace(dst)

    imgToBeConcat = img_[0:img_.shape[0]-trimmedDst.shape[0] :].copy()
    
    finalStitchedImage = cv2.vconcat([imgToBeConcat, img])

    seedPoints = [(10, 10), (10, img_.shape[0])]

    outputImg = floodFillBackground(finalStitchedImage, seedPoints, difference)

    cv2.imwrite(outputName, outputImg)


def hStitch(imgFileList, outputName):
    imgList = []
    for fileName in imgFileList:
        imgList.append(cv2.imread(fileName))

    hMin = min(img.shape[0] for img in imgList)
      
    imListResize = [cv2.resize(img, (int(img.shape[1] * hMin / img.shape[0]), hMin), interpolation = cv2.INTER_CUBIC) for img in imgList]

    cv2.imwrite(outputName, cv2.hconcat(imListResize))
