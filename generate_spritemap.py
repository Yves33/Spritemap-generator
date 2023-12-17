import json
import cv2
import numpy as np

ERODE_AND_DILATE=True
PYGLET_COORDINATES=True

def split(imgfile,mapfile,boxfile):
    image = cv2.imread(imgfile)                                                     ## open image
    blank=np.zeros(image.shape, dtype=np.uint8)                                     ## create a black image with same dimensions
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)                                  ## convert original to grayscale
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]## perform otsu thresholding
    if not ERODE_AND_DILATE:
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) ## get the contours
    else:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))                   ## or process image before
        close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
        dilate = cv2.dilate(close, kernel, iterations=1)
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) ## get the contours
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    rects=[]
    for idx,c in enumerate(cnts[::-1]):
        x,y,w,h = cv2.boundingRect(c)
        #ROI = image[y:y+h, x:x+w]
        #cv2.imwrite('sprite_{}.png'.format(idx), ROI)
        cv2.rectangle(blank, (x, y), (x + w, y + h), (36,255,12), 1)
        cv2.putText(blank,str(idx),(x+2,y+h-2),cv2.FONT_HERSHEY_SIMPLEX,0.4,(36,255,12),1)
        if PYGLET_COORDINATES:
            rects.append([x,image.shape[0]-y-h,w,h])
        else:
            rects.append([x,y,w,h])
    json.dump({"rectangles":rects},open(mapfile,"w+"))

    cv2.imshow('image', blank)
    cv2.waitKey()
    cv2.imwrite(boxfile,blank)

if __name__=='__main__':
    import sys,pathlib

    if len(sys.argv)>1:
        spritesheet=pathlib.Path(sys.argv[1])
    else:
        spritesheet=pathlib.Path('./resource/megaman_full.png')
    spritemap=str(spritesheet.parent/spritesheet.stem)+'.json'
    spritebox=str(spritesheet.parent/spritesheet.stem)+'_bbox.png'
    split(str(spritesheet),spritemap,spritebox)
