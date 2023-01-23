# PS1 dithering recreated in Python


The algorithm I'm using is based on HLSL code: https://gist.github.com/ompuco/3209f1b32213cec5b7bccf0e67caf3e9

Its author: https://twitter.com/ompuco

The difference is that at one point I'm clamping color values between 0 and 255 to prevent overflow. Also, I'm not using a shading language, but rather Python with `numpy` and `opencv` (so my version is **not realtime**)

# Examples (zoom in to clearly see the difference)

Th original images were 1024x1024. Dithering works on individual pixels, so it's most visible in lower resolutions. Therefore, both the original and dithered images were downscaled and upscaled, but dithered image was also dithered inbetween.


Original             |  Dithered
:-------------------------:|:-------------------------:
![out](https://user-images.githubusercontent.com/50328147/203868627-4068728c-d685-4b27-860d-79380f1ea1e0.png)  |  ![out_dithered3](https://user-images.githubusercontent.com/50328147/203868637-3dd832c3-993a-40a9-9591-2f64e6f290d4.png)
![out](https://user-images.githubusercontent.com/50328147/203868902-ad6b3319-3f5e-429a-bb72-0964e5282c88.png)  |  ![out_dithered4](https://user-images.githubusercontent.com/50328147/203868899-8b0ff0ec-7ba8-47e6-8fd3-40383ecc8449.png)

The models in these images were made by me in Blender.

# See also:
https://twitter.com/jazzmickle/status/1269238990827335689
(seemingly based on the same algorithm, but recreated in Unreal Engine)


# TODO: 
- check whether it's true that ompuco based this code on original PS1 algorithm.


