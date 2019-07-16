import cv2
import numpy as np

# Read image
img = cv2.imread("imori.jpg")

# val = {  32  (0 <= val < 63)
#          96  (63 <= val < 127)
#         160  (127 <= val < 191)
#         224  (191 <= val < 256)
# Dicrease color 色彩压缩
out = img.copy()

for i in range(4):
    ind = np.where(((64*i-1) <= out) & (out < (64*(i+1)-1)))
    out[ind] = 32 * (2*i+1)

# Save result
cv2.imwrite("out.jpg", out)
cv2.imshow("result", out)
cv2.waitKey(0)
cv2.destroyAllWindows()
