from OpenGL.GL import *

from enum import Enum
import pygame

class TEXTURE_WRAP(Enum):
    GL_CLAMP_TO_EDGE = GL_CLAMP_TO_EDGE
    GL_REPEAT = GL_REPEAT

# for use with pygame
def load_texture(path, param: TEXTURE_WRAP = TEXTURE_WRAP.GL_REPEAT):
    texture = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texture)
    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, param.value)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, param.value)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    # load image
    image = pygame.image.load(path)
    image = pygame.transform.flip(image, False, True)
    image_width, image_height = image.get_rect().size
    img_data = pygame.image.tostring(image, "RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return texture