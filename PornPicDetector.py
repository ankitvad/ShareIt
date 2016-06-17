'''
ref:
1.http://www.naun.org/multimedia/NAUN/computers/20-462.pdf
2.http://blog.csdn.net/gzlaiyonghao/article/details/3166735
from adultscanner import get_skin_ratio as gsr
from PornPicDetector import detector as ppd
'''
from PIL import Image
import sys
def image_ifo(image):
    try:
        img = Image.open(image)
        return img
    except Exception,e:
       return 0

def preprocessed_image(image):
    img = image_ifo(image)
    if not img:
        return 0
    if not img.mode == 'YCbCr':
        img = img.convert('YCbCr')
    return img

def detector(image):
    img = preprocessed_image(image)
    if not img:
        return 0
    ycbcr_data = img.getdata()
    W,H = img.size
    THRESHOLD = 0.3
    count = 0
    for i,ycbcr in enumerate(ycbcr_data):
        y,cb,cr = ycbcr
        #if 80 <= cb <= 120 and 133 <= cr <= 173:
        if 86 <= cb <= 127 and 130 <= cr < 168:
            count += 1
    if count > THRESHOLD*W*H:
        return "adult" #adult
    else:
        return "clean" #clean

if __name__ == '__main__':
    image = sys.argv[-1]
    print 'Detector is working on it,please wait a second...'
    detector(image)
    print 'Detecting is done!'

