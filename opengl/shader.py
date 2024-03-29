from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

SHADERS_PATH = "./opengl/"

DEFAULT_VERTEX = """
# version 330

layout(location = 0) in vec2 in_position;
layout(location = 1) in vec2 in_texcoord;

out vec2 uv;

void main()
{
    gl_Position = vec4(in_position, 0.0, 1.0);
    uv = in_texcoord;
}
"""

# FRAG_SRC = """
# # version 330

# out vec4 FragColor;

# void main()
# {
#     FragColor = vec4(1.,1.,0.,1.);  
# }
# """

class Shader:
    def __init__(self, name:str):
        #load fragment shader source
        with open(f"{SHADERS_PATH}{name}.frag", "r") as f:
            frag_src = f.read()
        v = compileShader(DEFAULT_VERTEX, GL_VERTEX_SHADER)
        f = compileShader(frag_src, GL_FRAGMENT_SHADER)
        self.program =  compileProgram(v, f)
        
    def use(self):
        glUseProgram(self.program)

    def set_mat4fv(self, uniform_name:str, value):
        loc = glGetUniformLocation(self.program, uniform_name)
        glUniformMatrix4fv(loc, 1, GL_FALSE, value)

    def set_float(self, uniform_name:str, value:float):
        loc = glGetUniformLocation(self.program, uniform_name)
        glUniform1f(loc, value)

    def set_vec2(self, uniform_name:str, v1,v2):   
        loc = glGetUniformLocation(self.program, uniform_name)
        glUniform2f(loc, v1, v2); 

    def set_int(self, uniform_name:str, value:int):
        loc = glGetUniformLocation(self.program, uniform_name)
        glUniform1i(loc, value)
