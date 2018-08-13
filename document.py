import cv2
import rect
import numpy as np

class Scanner(object):
    def __init__(self):
        pass
    def __del__(self):
        pass

    def auto_canny(self, image, sigma=0.33):
        v = np.median(image)
    
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(image, lower, upper)
    
        # return the edged image
        return edged

    
    def four_point_transform(self, image, rect):
        # obtain a consistent order of the points and unpack them
        # individually
        (tl, tr, br, bl) = rect
    
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
    
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
    

        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = "float32")
    
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    
        # return the warped image
        return warped

    
    def detect_edge(self, image, enabled_transform = False):
        dst = None
        orig = image.copy()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 0, 20)
        _, contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        for cnt in contours:
            epsilon = 0.051 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            if len(approx) == 4:
                target = approx
                cv2.drawContours(image, [target], -1, (0, 255, 0), 2)

                if enabled_transform:
                    approx = rect.rectify(target)
                    dst = self.four_point_transform(orig, approx)
                break

        return image, dst

        
