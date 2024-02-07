import cv2
import numpy as np

def gaussian(image, level):

    gaussian = [image]

    for i in range(level - 1):
        image = cv2.GaussianBlur(image, (5, 5),0)
        image = image[::2, ::2]
        gaussian.append(image)

    return gaussian


def custom_upsample(image):

    height, width = image.shape[:2]
    return cv2.resize(image, (2 * width, 2 * height), interpolation=cv2.INTER_LINEAR)


def custom_downsample(image):
    return image[::2, ::2]



def laplacian(gaussian, level):

    laplacian = [gaussian[level - 1]]

    for i in range(level - 1, 0, -1):

        upsampled = custom_upsample(gaussian[i])
        upsampled = upsampled[:gaussian[i - 1].shape[0], :gaussian[i - 1].shape[1]]
        L1 = cv2.subtract(gaussian[i - 1], upsampled)
        laplacian.append(L1)

    return laplacian


def blend_images(image1, image2, mask):
    image1 = image1.astype(np.float32)
    image2 = image2.astype(np.float32)
    mask = mask.astype(np.float32) / 255.0

    blended_image = image1 * (1 - mask) + image2 * mask

    blended_image = np.clip(blended_image, 0, 255).astype(np.uint8)

    return blended_image


def blend_pyramids(laplacian1, laplacian2, mask):

    blended_pyramid = []

    for l1, l2 ,g in zip(laplacian1, laplacian2, mask):
        l2 = cv2.resize(l2, (l1.shape[1], l1.shape[0]))
        resized_mask = cv2.resize(g, (l2.shape[1], l2.shape[0]))

        blended_level = blend_images(l1, l2, resized_mask)

        blended_pyramid.append(blended_level)

    return blended_pyramid




def collapse_pyramid(pyramid):
    image = pyramid[-1]

    for level in reversed(pyramid[:-1]):
        expanded_image = custom_upsample(image)

        level = cv2.resize(level, (expanded_image.shape[1], expanded_image.shape[0]))

        image = cv2.add(expanded_image, level)

    return image


def move_mask(image, mask, dx, dy):

    translation_matrix = np.float32([[1, 0, dx], [0, 1, dy]])

    image_translated = cv2.warpAffine(image, translation_matrix, (image.shape[1], image.shape[0]))
    mask_translated = cv2.warpAffine(mask, translation_matrix, (mask.shape[1], mask.shape[0]))

    return image_translated, mask_translated





A = cv2.imread(r"../{folder}/{file}.jpg") #image to be blended with the mask
B = cv2.imread(r"../{folder}/{file}.jpg") #image to be masked

roi = cv2.selectROI('Select ROI', B, fromCenter=False, showCrosshair=True)
cv2.destroyWindow('Select ROI')

# Extract the selected region from the input image
x, y, w, h = roi
roi_image = B[y:y+h, x:x+w]

# Create a binary mask from the selected ROI
mask = np.zeros_like(B, dtype=np.uint8)
mask[y:y+h, x:x+w] = 255

# Apply the mask to the input image
masked_image = cv2.bitwise_and(B, mask)

min_rows = min(A.shape[0], B.shape[0])
min_cols = min(A.shape[1], B.shape[1])

A = cv2.resize(A, (min_cols, min_rows))
B = cv2.resize(B, (min_cols, min_rows))
masked_image = cv2.resize(masked_image, (min_cols, min_rows))


#Coordinates for moving the mask
dx =1  # -1 => shift left , +1 => shift right the mask
dy =1  # -1 => scrolls down , +1 => scrolls up the mask

# Move the mask on the image
image_moved, mask_moved = move_mask(B, mask, dx, dy)

#Pramids Level
level=5


gaussianA = gaussian(A, level)
laplacianA = laplacian(gaussianA, level)

gaussianB = gaussian(image_moved, level)
laplacianB = laplacian(gaussianB, level)

gaussianMask = gaussian(mask_moved, level)

blended_pyramid = blend_pyramids(laplacianA, laplacianB, gaussianMask)

result_image = collapse_pyramid(blended_pyramid)



cv2.imshow('Blended Image', result_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
