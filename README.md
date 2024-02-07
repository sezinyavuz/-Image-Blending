# Image Blending
The goal of this assignment is to obtain a blended image from the input image


###Introduction

This Python script demonstrates a method for seamlessly blending two images with a smooth transition between selected regions using Laplacian Pyramids and mask translation.

### Requirements

- Python 3.x
- OpenCV (cv2)
- NumPy


### Usage

1. Install the required dependencies:

   ```bash
   pip install opencv-python numpy

2. Replace the placeholder in the image file path (`"../{folder}/{file}.jpg"`) according to the path of the input files you downloaded from the google drive link I added below.

-Google Drive Links:

	Input images:
	https://drive.google.com/drive/folders/1cMFOVZECulR1N6_5e7DxAWJt7bDtKQFM?usp=sharing

	In links there are seven seven image input pair and two single input.you should paste the paths of images after downloading the folder to the(line 96)
 
"A = cv2.imread(r"../{folder}/{file}.jpg") ##image to be blended with the mask
 B = cv2.imread(r"../{folder}/{file}.jpg”) ##image to be masked” 

part of the code. ‘A’ for the first input, ‘B’ for the second input. For single input image you should paste the same path for ‘A’ and ’B’.

	All inputs, masks and outputs:
    https://drive.google.com/drive/folders/1JG6-SN3clLIuuCQm31KuZ8GOK3_cha4j?usp=sharing


3. Before run the code, you should determine pyramids level(line129) and coordinates dx, dy(line 122) where you want to blend the mask with image(A).Then, run the code to execute the image blending tasks.



### Instructions

1. The script will display an interactive window allowing you to select a region of interest (ROI) in one of the input images. Use the mouse to draw a rectangle around the desired area.
2. The selected ROI will be used to create a binary mask, isolating the chosen portion of the image.
3. The script then resizes both images to a common size for consistency.
4. The mask is translated over one of the images using specified translation parameters (`dx` and `dy`). You can determine the coordinates yourself.
5. You can determine the pyramids level manually.
6. Laplacian Pyramids are constructed for both images to represent the image details at different scales.
7. The blending is performed at each pyramid level using the translated mask, creating smooth transitions between the images.
8. The final blended image is reconstructed by collapsing the blended Laplacian Pyramids.

### Additional Notes
- The script includes functions for Gaussian and Laplacian pyramid construction, custom upsampling and downsampling, image blending, and mask translation.
- You can customize the `dx` and `dy` variables to control the translation of the mask.
- The script utilizes OpenCV for image processing and NumPy for array manipulation.

### Output
- The final blended image is displayed.


### Author
Sezin Yavuz
