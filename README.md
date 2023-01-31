# PlayStation 1 dithering ported to GLSL and Python

## Inspiration
The algorithm I'm using is based on HLSL code: https://gist.github.com/ompuco/3209f1b32213cec5b7bccf0e67caf3e9 \
Its author: https://twitter.com/ompuco

See also: https://twitter.com/jazzmickle/status/1269238990827335689 \
(seemingly based on the same algorithm, but recreated in Unreal Engine)

## Differences between the original

- The difference is that at one point I'm clamping color values between 0 and 255 to prevent overflow (I guess PS1 simply wasn't using values that could overflow as a result of dithering; or overflow was somehow prevented, idk).

- Also, I've added a not-realtime version in which I'm not using a shading language, but rather Python with `numpy` and `opencv`.

# Dithered examples

***(zoom in to clearly see the difference)***

Dithering works on individual pixels, so it's most visible in lower resolutions. Therefore the example images were:
- in Python version: downscaled, dithered and upscaled back.
- in GLSL version: pixelated in fragment shader without changing image resolution.

Original             |  Dithered
:-------------------------:|:-------------------------:
![DesertGiants_downscaled](https://user-images.githubusercontent.com/50328147/215885437-4faff45d-d266-4475-a03e-0248be271d3c.png) | ![imgg2](https://user-images.githubusercontent.com/50328147/215885339-f691669c-6039-4eb4-acde-c328b4475572.png)
![UV_downscale](https://user-images.githubusercontent.com/50328147/215885470-f39a78c7-4466-4665-b3af-2bdb64fd1229.png) | ![imgg](https://user-images.githubusercontent.com/50328147/215885324-8d35b097-b2b9-4106-bf47-1655c12361b2.png)

# Repository's file structure

- `example_images/` (example images you can use for testing the dithering)
- `opengl/`
    - `main.py`, `shader.py`, `texture.py` (OpenGL boilerplate)
    - `ps1_dither.frag` (GLSL shader responsible for dithering)
- `python/main.py` (the only script responsible for dithering in Python)

# Usage 

***(only tested on Windows)***

Install all dependencies: 
- `pip install -r requirements.txt`

**GLSL** version: 
- `python ./opengl/main.py  <image-input-path> <image-output-path> <downscale-factor>`

**Python** version: 
- `python ./python/main.py  <image-input-path> <image-output-path> <downscale-factor>`

See **help** for documentation: 
- `python ./opengl/main.py --help` 
- `python ./python/main.py --help`


Concrete examples: 
- `python ./opengl/main.py  example_images/DesertGiants.png ./ 3 --no-display` \
(uses GLSL; takes `DesertGiants.png` image, downscales the resolution 8 times (==2^3) and saves it in the CWD immediately without showing the output image to the user) 
- `python ./opengl/main.py  example_images/DesertGiants.png ./ 3 --display` \
(uses GLSL; same as above, but the image is first displayed to the user; it is saved to CWD only after the display window is closed) 
- `python ./python/main.py  example_images/UV.png C:/Users/someimg.png 1` \
(uses Python; takes `UV.png` image, downscales the resolution 2 times (==2^1) and saves it as `C:/Users/someimg.png`) 



# TODO (contributions welcome)
- check whether it's true that ompuco based this code on original PS1 algorithm.
- Python and GLSL versions produce slightly different output - seems like pixels in output images are shifted by a pixel or two; or maybe there is even some discrepancy in dithering - not sure. I'm thinking that maybe it's a matter of scaling and casting floating point precision variables, which produces this discrepancy. Anyways, it's worth investigating. 
- check whether it works on Linux and MacOS


