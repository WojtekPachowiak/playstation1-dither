import os
import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from texture import load_texture_pygame, TEXTURE_WRAP, generate_framebuffer
import glm
import numpy as np
from shader import Shader
from constants import WIDTH, HEIGHT


pygame.init()
# pygame.display.gl_set_attribute(pygame.GL_STENCIL_SIZE, 8)
pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE) # |pygame.FULLSCREEN




def add_screenquad():
    '''add a quad that fills the entire screen'''
    #buffer in Normalized Device Coordinates
    vertices = np.array([ 
        #positions   #texCoords
        -1.0,  1.0,  0.0, 1.0,
        -1.0, -1.0,  0.0, 0.0,
         1.0, -1.0,  1.0, 0.0,

        -1.0,  1.0,  0.0, 1.0,
         1.0, -1.0,  1.0, 0.0,
         1.0,  1.0,  1.0, 1.0
    ],dtype=np.float32)
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * vertices.itemsize, ctypes.c_void_p(0));
    glEnableVertexAttribArray(1);
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * vertices.itemsize, ctypes.c_void_p(8));
    glBindVertexArray(0)
    return vao


texture_shader = Shader("ps1_dither")

screenquad_vao = add_screenquad()

textures = glGenTextures(5)
load_texture_pygame("textures/example_img.png", textures[0])

projection = glm.ortho(-10.0, 10.0, -10.0, 10.0, 0.1, 10)
view = glm.lookAt(glm.vec3([0.0, 0.0, 0.0]), glm.vec3([0.0, 0.0, -1.0]), glm.vec3([0.0, 1.0, 0.0]));

def screenshot():
    screen = pygame.display.get_surface()
    size = screen.get_size()
    buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
    screen_surf = pygame.image.fromstring(buffer, size, "RGBA", True)
    pygame.image.save(screen_surf, "screenshot.png")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif  event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_s:
                screenshot()

        # if event.type == pygame.VIDEORESIZE:
        #     # glViewport(0, 0, event.w, event.h)
        #     projection = glm.perspective(45, event.w / event.h, 0.1, 100)
        
    ct = pygame.time.get_ticks() / 1000

    texture_shader.use()
    texture_shader.set_mat4fv("view", glm.value_ptr(view))
    texture_shader.set_mat4fv("projection", glm.value_ptr(projection))


    glClearColor(1.0, 0.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    
    texture_shader.use()
    glBindVertexArray(screenquad_vao)
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glDrawArrays(GL_TRIANGLES, 0, 6)
    
    pygame.display.flip()

pygame.quit()

