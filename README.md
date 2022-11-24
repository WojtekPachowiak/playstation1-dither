# PlayStation-1-dithering
PS1 dithering recreated in Python

The algorithm I'm using is based on:

https://gist.github.com/ompuco/3209f1b32213cec5b7bccf0e67caf3e9

The only difference is that at one point I'm clamping color values between 0 and 255 to prevent overflow.


### TODO: 
- check whether it's true that ompuco based this code on original PS1 algorithm.


