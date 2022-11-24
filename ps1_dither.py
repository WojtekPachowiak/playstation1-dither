import numpy as np
import cv2 as cv


FILE_PATH = f'<path_to_image>'
OUTPUT_FILE_PATH = '//Dither_mod.png'


def main():
    img = load_image(FILE_PATH)
    print('Image loaded!')
    #scale the image between dithering
    # img = scale(img)
    img = dither(img)
    save_image(img)
    print('Image saved!')

def scale(img, res :tuple[int,int]):
    'scale image using nearest interpolation'
    img = cv.resize(img, res, interpolation = cv.INTER_NEAREST )
    return img

def load_image(file_path):
    print('Loading image...')
    return cv.imread(file_path, cv.IMREAD_COLOR) 

def save_image(image):
    cv.imwrite(OUTPUT_FILE_PATH, image)

def dither(img):
    'the dither algorithm'
    #convert pixel values to floats
    img = img.astype(float)

    dither_matrix = np.array([
            0,    8,    2,    10,
            12,    4,    14,    6, 
            3,    11,    1,    9, 
            15,    7,    13,    5
        ],dtype=float).reshape(4,4);

    #tile dither_matrix to image size
    dither = np.tile(dither_matrix, np.array(img.shape[:2])//np.array(np.shape(dither_matrix)) + 1)[:img.shape[0], :img.shape[1]]

    #for example:
    # tiling the following (2,2) matrix:
    # [1,2]
    # [3,4]
    # to (5,5) image size would result in the following matrix:
    # [1,2,1,2,1]
    # [3,4,3,4,3]
    # [1,2,1,2,1]
    # [3,4,3,4,3]
    # [1,2,1,2,1]

    #expand shape from (x,y) to (x,y,1)
    dither = np.expand_dims(dither,axis=2)
    
    ### the meat of the algorithm starts here ###
    img += (dither / 2.0 - 4.0)
    t = img >= 0xf8
    #clipping pixel values between 0-255 then casting to uint8. Otherwise some values would overflow (very dark would became very light and the other way round)
    img = np.clip(img, 0, 255).astype(np.uint8) 
    # this is a lerp function
    img = (img & 0xf8)*(1-t) + 0xf8 * t

    return img
    


