import skimage.io as ski
import skimage.filters as skif
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def estimate_hemoglobin_level(binary_img):
    """
    Estimate hemoglobin levels based on the intensity of binary image pixels.
    """
    # Calculate the ratio of white pixels to total pixels
    white_pixels = np.sum(binary_img == 255)  # Count white pixels
    total_pixels = binary_img.size  # Total number of pixels
    white_ratio = white_pixels / total_pixels

    # Assume hemoglobin level proxy based on white ratio (simple proxy logic)
    hemoglobin_level = white_ratio * 20  # Scaled to approximate 0-20 g/dL (example range)

    # Determine the category based on thresholds
    if hemoglobin_level < 12:
        category = "Low Hemoglobin"
    elif 12 <= hemoglobin_level <= 16:
        category = "Normal Hemoglobin"
    else:
        category = "High Hemoglobin"

    return hemoglobin_level, category

# INPUT IMAGE
img_path = os.path.join(os.getcwd(), 'd.jpg')  # Replace 'a.jpg' with your image filename
img1 = ski.imread(img_path)

# Convert to Grayscale using OpenCV
gray_img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

# Otsu's Thresholding: Calculate threshold value using skimage
t = skif.threshold_otsu(gray_img)
print(f"Threshold Value: {t}")

# Convert to Binary Image: Using threshold
_, binary_img = cv2.threshold(gray_img, t, 255, cv2.THRESH_BINARY)

# Estimate hemoglobin levels
hemoglobin_level, category = estimate_hemoglobin_level(binary_img)
print(f"Estimated Hemoglobin Level: {hemoglobin_level:.2f} g/dL")
print(f"Category: {category}")

# Display the Binary Image
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title("Original Grayscale Image")
plt.imshow(gray_img, cmap="gray")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.title(f"Binary Image\n(Hemoglobin: {hemoglobin_level:.2f} g/dL - {category})")
plt.imshow(binary_img, cmap="gray")
plt.axis("off")
plt.tight_layout()
plt.show()
