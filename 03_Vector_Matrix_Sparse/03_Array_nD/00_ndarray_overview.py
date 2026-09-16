'''
ndarray is a general term describes high-dimension array (more than 2D).

Several ndarray types that you would usually encounter are:
    + 3D array: an image           (channel, high, width)
    + 4D array: a batche of images (num_images, channel, height, width)
'''

import numpy as np

# =========================================
# 1. Example of 3D array
# =========================================
'''
Modern digital images often use 3D arrays to represent color images.
For example, an RGB image with 3 channels (Red, Green, Blue) can be represented as a 3D array.

Each R, G and B channel is a 2D matrix representing pixel intensities.
Combining these 2D matrices along a new dimension (channel) forms a 3D matrix.
'''

CHANNELS = 3  # RGB
HEIGHT = 4
WIDTH = 8

np.random.seed(0)
image_3d = np.random.randint(0, 256, size=(CHANNELS, HEIGHT, WIDTH), dtype=np.uint8)

print(image_3d)
'''
[[[172  10 127 140  47 170 196 151]
  [117 166  22 183 192 204  33 216]               # Red channel
  [ 67 179  78 154 251  82 162 219]
  [195 118 125 139 103 125 229 216]]

 [[  9 164 116 108 211 222 161 159]
  [ 21  81  89 165 242 214 102  98]               # Green channel
  [ 36 183   5 112  87  58  43  76]
  [ 70  60  75 228 216 189 132  14]]

 [[ 88 154 178 246 140 205 204  69]
  [ 58  57  41  98 193  66  72 122]               # Blue channel
  [230 125 174 202  39  74 234 207]
  [ 87 168 101 135 174 200 223 122]]]
'''
# Can use matplotlib to visualize this 3D array as an image if needed.

print(image_3d.shape)
# (3, 4, 8)

# ============================================================================
# 2. Example of 4D array
# ============================================================================
'''
Each image is represented as a 3D array (channel, height, width).
Stacking multiple images along a new dimension (num_images) forms a 4D array.
'''

NUM_IMAGES = 4
CHANNELS = 3  # RGB
HEIGHT = 2
WIDTH = 3

np.random.seed(1)
images_4d = np.random.randint(0, 256, size=(NUM_IMAGES, CHANNELS, HEIGHT, WIDTH), dtype=np.uint8)

print(images_4d)
'''
[[[[ 37 244 193]
   [106 235 128]]

  [[ 71 255 140]
   [ 47 103 184]]                     # Image 1

  [[ 72  20 188]
   [238 255 126]]]

 [[[  7   0 137]
   [195 204  32]]

  [[203 170 101]
   [ 77 133  30]]                     # Image 2

  [[193 255  79]
   [203 145  37]]]

 [[[192  83 112]
   [ 60 144 128]]

  [[163  23 129]
   [ 80 134 101]]                     # Image 3

  [[204 191 174]
   [ 47  71  30]]]

 [[[ 78  99 237]
   [170 118  88]]

  [[252 121 116]
   [171 134 141]]                    # Image 4

  [[146 101  25]
   [125 127 239]]]]
'''

print(images_4d.shape)
# (4, 3, 2, 3)
