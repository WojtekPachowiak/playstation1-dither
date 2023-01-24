# version 330


#define useDither 1

in vec2 uv;
out vec4 FragColor;

uniform sampler2D u_texture_0; // ./dither_matrix.png
uniform sampler2D u_texture_1; // ./example_img.png
uniform vec2 u_resolution;

// vec3 float_bitwise_AND(vec3 a, float b){
//     // x : some number
//     // n : 2 exponent (2^n)

//     //bit mask
//     float n = log2(b+1.);
//     float mask = pow(2., n);
//     return fract(a/mask)*(mask);
// }

mat4 psx_dither_table=mat4
(
    0,8,2,10,
    12,4,14,6,
    3,11,1,9,
    15,7,13,5
);

float dither_table(int col, int row){
  // return psx_dither_table[col][row]
  return texture(u_texture_0, vec2(col,row)).r;
}

vec3 dither(vec3 color, vec2 p){
    color*=255.;//extrapolate 16bit color float to 16bit integer space
    if(useDither==1)
    {
        highp int col = int(mod(p.x, 4.));
        highp int row= int(mod(p.y, 4.));
        // color = vec3(col, row,0.) ;
        // color = vec3(dither_table(col,row))*1000.;
        float dither = psx_dither_table[col][row];
        color += (dither/2. - 4.);//dithering process as described in PSYDEV SDK documentation
        color = max(color,0.);
    }
    
    ivec3 c = ivec3(color) & ivec3(0xf8);
    color = mix( vec3(c), vec3(0xf8),  step(vec3(0xf8),color) );
    // ivec3 t = ivec3(step(vec3(0xf8),vec3(color) ));
    // color = vec3(c * (1-t) + 0xf8 * t);
    // color = vec3(mix( c, vec3(0xf8),  step(vec3(0xf8),color ));
    // color = vec3(t);
  
    // color = float_bitwise_AND(color, b_0xf8);
    //truncate to 5bpc precision via bitwise AND operator, and limit value max to prevent wrapping.
    //PS1 colors in default color mode have a maximum integer value of 248 (0xf8)
    color/=255.; //bring color back to floating point number space
    return color;
}

void main() {
  vec3 color= texture(u_texture_1,  uv).rgb; 
  color = dither(color, gl_FragCoord.xy);
  
  // vec4 color = vec4(vec3(uv.x),1.);
  
  // Send the color to the screen
  FragColor=vec4(color,1.);

}