
/* Main function, uniforms & utils */
#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform vec2 u_mouse;



//PS1 dither table from PSYDEV SDK documentation
mat4 psx_dither_table=mat4
(
    0,8,2,10,
    12,4,14,6,
    3,11,1,9,
    15,7,13,5
);
//if desired, this can also be stored as an int4x4


int modulo(int a,int b){
    float a_f=float(a);
    float b_f=float(b);
    return int(a_f-(b_f*floor(a_f/b_f)));
}






float dither_table(int col, int row){
    if (col == 0){
       if (row == 0) return 0.; 
       else if (row == 1) return 12.; 
       else if (row == 2) return 3.; 
       else if (row == 3) return 15.; 
    }
    else if (col == 1){
       if (row == 0) return 8.; 
       else if (row == 1) return 4.; 
       else if (row == 2) return 11.; 
       else if (row == 3) return 7.; 
    }
    else if (col == 2){
       if (row == 0) return 2.; 
       else if (row == 1) return 14.; 
       else if (row == 2) return 1.; 
       else if (row == 3) return 13.; 
    }
    else if (col == 3){
       if (row == 0) return 10.; 
       else if (row == 1) return 6.; 
       else if (row == 2) return 9.; 
       else if (row == 3) return 5.; 
    }
}

// x & (2^n)-1 = frac(x/(2^n))*(2^n)

// (2^n)-1 = 248
// n = log2(249)

//source: https://stackoverflow.com/a/1700928
vec3 float_bitwise_AND(vec3 a, float b){
    // x : some number
    // n : 2 exponent (2^n)

    //bit mask
    float n = log2(b+1.);
    float mask = pow(2., n);
    return fract(a/mask)*(mask);
}

#define b_0xf8 248.0
#define useDither 0//set to 0 to disable dithering and only truncate raw color input

//col - your high-precision color input
//p - screen position in pixel space
vec3 dither(vec3 color,ivec2 p){
    color*=255.;//extrapolate 16bit color float to 16bit integer space
    if(useDither==1)
    {
        int col= modulo(p.x,4);
        int row= modulo(p.y,4);
        float dither=dither_table(col,row);
        color+=(dither/2.-4.);//dithering process as described in PSYDEV SDK documentation
    }
    color = mix( float_bitwise_AND(color, b_0xf8)     ,  vec3(b_0xf8),  step(b_0xf8,color) );
    // color = float_bitwise_AND(color, b_0xf8);
    //truncate to 5bpc precision via bitwise AND operator, and limit value max to prevent wrapping.
    //PS1 colors in default color mode have a maximum integer value of 248 (0xf8)
    color/=255.;//bring color back to floating point number space
    return color;
}

vec2 pixelate(vec2 st){
    return mod(st,0.5);
}
void main(){
    vec2 st = gl_FragCoord.xy/u_resolution.xy;
    // st = pixelate(st);
    vec3 color=vec3(st.x);
    color=dither(color,ivec2(gl_FragCoord.xy));
    gl_FragColor=vec4(color,1.);
}