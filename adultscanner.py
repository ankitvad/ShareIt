#!python2

import os, glob
from PIL import Image

def get_skin_ratio(image_file):
    im = Image.open(image_file)
    im = im.crop((int(im.size[0]*0.2), int(im.size[1]*0.2), im.size[0]-int(im.size[0]*0.2), im.size[1]-int(im.size[1]*0.2)))
    skin = sum([count for count, rgb in im.getcolors(im.size[0]*im.size[1]) if rgb[0]>60 and rgb[1]<(rgb[0]*0.85) and rgb[2]<(rgb[0]*0.7) and rgb[1]>(rgb[0]*0.4) and rgb[2]>(rgb[0]*0.2)])
    return float(skin)/float(im.size[0]*im.size[1])

'''
for image_dir in ('adult','clean','image_23','abc'):
    for image_file in glob.glob(os.path.join(image_dir,"*.jpg")):
        skin_percent = get_skin_ratio(Image.open(image_file)) * 100
        is_porn = skin_percent>30
        if is_porn:
            print "ADULT {0} has {1:.0f}% skin".format(image_file, skin_percent)
        else:
            print "CLEAN {0} has {1:.0f}% skin".format(image_file, skin_percent)
'''