import cv2
import pytesseract
import numpy as np

# Set tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Load image
image = cv2.imread('car.jpg')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Reduce noise
gray = cv2.bilateralFilter(gray, 11, 17, 17)

# Edge detection
edged = cv2.Canny(gray, 30, 200)

# Find contours
contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

plate = None

# Detect plate contour
for contour in contours:
    approx = cv2.approxPolyDP(contour, 10, True)
    if len(approx) == 4:
        plate = approx
        break

# Mask plate region
mask = np.zeros(gray.shape, np.uint8)
cv2.drawContours(mask, [plate], 0, 255, -1)
plate_img = cv2.bitwise_and(image, image, mask=mask)

# OCR Recognition
text = pytesseract.image_to_string(plate_img, config='--psm 8')
print("Detected Number:", text)

# Display image
cv2.imshow("Plate Detection", plate_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
