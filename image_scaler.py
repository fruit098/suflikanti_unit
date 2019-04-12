from os import listdir
from os.path import realpath, isfile,join

from PIL import Image

from resizeimage import resizeimage

instagram_format = [864,1080]
facebook_format = [1920,1080]

def scale_images(path_to_folder):
    """ 
        scale image for instagram and facebook
        instagram format => 864(width) : 1080(height) (4:5)
        facebook format => 1920 x 1080 ( 16 : 9 )

        generate images with prefix instagram_/facebook_
    """

    folder = realpath(path_to_folder)

    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
    
    folder += "/"

    for filename in onlyfiles:
        with open(folder + filename, "r+b") as f:
                with Image.open(f) as image:
                    if ( check_size_facebook(image) ):
                        facebook_cover = resizeimage.resize_cover(image, facebook_format)
                        facebook_cover.save(folder + "facebook_" + filename, image.format)

                    if ( check_size_instagram(image) ):
                        instagram_cover = resizeimage.resize_cover(image, instagram_format)
                        instagram_cover.save(folder + "instagram_" + filename, image.format)
                    


def check_size_instagram(img):
    size = img.size
    if ( size[0] < instagram_format[0] or size[1] < instagram_format[1] ):
        return False

    return True

def check_size_facebook(img):
    size = img.size
    if ( size[0] < facebook_format[0] or size[1] < facebook_format[1] ):
        return False

    return True
