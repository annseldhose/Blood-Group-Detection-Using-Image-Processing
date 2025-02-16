import skimage
import skimage.io as ski
import skimage.filters as skif
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# INPUT IMAGE
img1 = ski.imread(os.path.join(os.getcwd(), 'a.jpg'))

# Convert to Grayscale using OpenCV
gray_img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

# Otsu's Thresholding: Calculate threshold value using skimage
t = skif.threshold_otsu(gray_img)
print(f"Threshold Value: {t}")

# Convert to Binary Image: Using threshold
_, binary_img = cv2.threshold(gray_img, t, 255, cv2.THRESH_BINARY)

# Display the Binary Image
plt.imshow(binary_img, cmap="gray")
plt.show()
