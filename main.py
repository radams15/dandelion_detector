import numpy as np
import cv2
import esky
import sys

if getattr(sys,"frozen",False):
    #app = esky.Esky(sys.executable,"https://example-app.com/downloads/")
    app = esky.Esky(sys.executable,"http://localhost:8000")
    try:
        app.auto_update()
    except Exception as e:
        print ("ERROR UPDATING APP:", e)

def rgb2bgr(*rgb):
    return [rgb[2], rgb[1], rgb[0]]

if __name__ == '__main__':
    img = "image.JPG"

    out_file = "out.jpg"
    view = False
    save = True

    image = cv2.imread(img)

    # more fine increase this V
    lower, upper = [rgb2bgr(240, 0, 0), rgb2bgr(255, 255, 120)]#[rgb2bgr(233, 0, 0), rgb2bgr(255, 255, 120)]

    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    height_orig, width_orig = image.shape[:2]

    # output image with contours
    image_contours = image.copy()

    # DETECTING BLUE AND WHITE COLONIES

    # copy of original image
    image_to_process = image.copy()

    # initializes counter
    counter = 0

    # find the colors within the specified boundaries
    image_mask = cv2.inRange(image_to_process, lower, upper)
    # apply the mask
    image_res = cv2.bitwise_and(image_to_process, image_to_process, mask=image_mask)

    ## load the image, convert it to grayscale, and blur it slightly
    image_gray = cv2.cvtColor(image_res, cv2.COLOR_BGR2GRAY)
    image_gray = cv2.GaussianBlur(image_gray, (5, 5), 0)

    # perform edge detection, then perform a dilation + erosion to close gaps in between object edges
    image_edged = cv2.Canny(image_gray, 50, 100)
    image_edged = cv2.dilate(image_edged, None, iterations=1)
    image_edged = cv2.erode(image_edged, None, iterations=1)

    # find contours in the edge map
    cnts = cv2.findContours(image_edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0]# if imutils.is_cv2() else cnts[1]

    # loop over the contours individually
    for c in cnts:
        # if the contour is not sufficiently large, ignore it
        #if cv2.contourArea(c) < 5:
        #    continue

        # compute the Convex Hull of the contour
        hull = cv2.convexHull(c)

        # prints contours in red color
        #cv2.drawContours(image_contours, [hull], 0, (0, 0, 255), thickness=1)
        #cv2.circle(image_contours, center=tuple(c[0][0]), color=(0,0,255), thickness=1, radius=3)
        cv2.circle(image_contours, center=tuple(c[0][0]), color=(0,0,255), thickness=cv2.FILLED, radius=3)

        counter += 1
        # cv2.putText(image_contours, "{:.0f}".format(cv2.contourArea(c)), (int(hull[0][0][0]), int(hull[0][0][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

    # Print the number of colonies of each color

    print(f"Counted Approximately {counter} Dandelions")

    # Writes the output image
    image_out = image_contours
    if view:
        cv2.imshow("Edited", image_out)
        cv2.waitKey(0)
    if save:
        cv2.imwrite(out_file, image_out)