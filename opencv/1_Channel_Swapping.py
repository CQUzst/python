import cv2

# Read image
img = cv2.imread("imori.jpg")
img_1 = img.copy()
cv2.imshow("origin_img",img)
b = img[:, :, 0].copy()
g = img[:, :, 1].copy()
r = img[:, :, 2].copy()

# RGB > BGR
img[:, :, 0] = r
img[:, :, 1] = g
img[:, :, 2] = b

# You could use cv2.cvtColor() function to directly swap the color channels.
# img_rgb = cv2.cvtColor(img_1, cv2.COLOR_BGR2RGB)
# # cv2.imshow("img_rgb", img_rgb)

# Save result
# cv2.imwrite("out.jpg", img)
cv2.imshow("result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
