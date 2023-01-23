import numpy as np
import cv2 as cv


FILE_PATH = r'./morrigantest4_new.png'
OUTPUT_FILE_PATH = './out.png'
SCALE_EXPONENT = 2

def main():
    img = load_image(FILE_PATH)
    print('Image loaded!')
    # scale down the image before dithering
    img = scale(img, -SCALE_EXPONENT)
    #dither
    img = dither(img)
    # scale up the image before dithering
    img = scale(img, SCALE_EXPONENT)
    save_image(img)
    print('Image saved!')

def scale(img, scale=0):
    'scale image using nearest interpolation'
    img = cv.resize(img, (np.array(img.shape[:2])*(2**scale)).astype(int), interpolation = cv.INTER_NEAREST )
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
    
if __name__ == "__main__":
    main()

