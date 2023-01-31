import os
import pygame
from OpenGL.GL import *
from texture import load_texture
import numpy as np
from shader import Shader
import typer
from pathlib import Path



def main(
    input_file_path: str = typer.Argument(..., help="Path to input image"), 
    output_file_path: str = typer.Argument(..., help="Path where resulting image will be output"), 
    downscale_factor:int = typer.Argument(0, help="2's exponent determining how much to downscale (pixelate) the image in order to make the dithering more visible. Default is 0 which means no downscaling. WARNING! It doesn't change the reoslution of the output image."),
    display: bool = typer.Option(True, help="Whether to display the dithered image in a window before saving it"),
    dither: bool = typer.Option(True, help="Whether to dither the image or not")):
    
    assert downscale_factor >= 0, "downscale_factor must be a non-negative integer"


    WIDTH, HEIGHT = 1080,1080

    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE) # |pygame.FULLSCREEN

    def screenshot():
        ''' save the current viewport image to a file '''
        screen = pygame.display.get_surface()
        size = screen.get_size()
        buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        screen_surf = pygame.image.fromstring(buffer, size, "RGBA", True)
        pygame.image.save(screen_surf, output_file_path )

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


    shader = Shader("ps1_dither")
    shader.use()
    shader.set_float("u_downscale_factor", 2**downscale_factor)
    shader.set_vec2("u_resolution", WIDTH, HEIGHT)
    shader.set_int("u_dither", int(dither))



    texture = load_texture(input_file_path)
    screenquad_vao = add_screenquad()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif  event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False                    
            # if event.type == pygame.VIDEORESIZE:
            #     WIDTH, HEIGHT = event.w, event.h
            #     glViewport(0, 0, event.w, event.h)
            

        glClearColor(1.0, 0.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        
        shader.use()
        shader.set_vec2("u_resolution", WIDTH, HEIGHT)
        glBindVertexArray(screenquad_vao)
        glBindTexture(GL_TEXTURE_2D, texture)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        

        if display == False or running == False:  
            running = False
            #take a screenshot
            screenshot()

        pygame.display.flip()
        
    pygame.quit()


if __name__ == "__main__":
    typer.run(main)
