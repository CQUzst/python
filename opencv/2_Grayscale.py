import cv2
import numpy as np

# Read image
img = cv2.imread("imori.jpg")
img_origion = img.copy()
img = img.astype(np.float)
b = img[:, :, 0].copy()
g = img[:, :, 1].copy()
r = img[:, :, 2].copy()

# Grayscale
# You could use the cv2.cvtColor() to change the rgb image into grayscale.
# gray = cv2.cvtColor(img_origion, cv2.COLOR_BGR2GRAY)
# cv2.imshow("gray",gray)


out = 0.2126 * r + 0.7152 * g + 0.0722 * b
out = out.astype(np.uint8)

# Save result
cv2.imwrite("out.jpg", out)
cv2.imshow("result", out)
cv2.waitKey(0)
cv2.destroyAllWindows()
