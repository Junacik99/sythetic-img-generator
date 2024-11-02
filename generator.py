import cv2
import numpy as np
import random
import os

src_dir = 'img'
dst_dir = 'output'

def lighting_effect(img, brightness=1.0, contrast=1.0, shadow_intensity=0.3):
	# Adjust brightness and contrast
	img = cv2.convertScaleAbs(img, alpha=contrast, beta=int((brightness - 1) * 128))

	# Adding shadow effect
	shadow_overlay = np.zeros_like(img, dtype=np.uint8)
	rows, cols = img.shape[:2]
	shadow_center = (random.randint(0, cols), random.randint(0, rows))
	shadow_radius = random.randint(min(rows, cols) // 4, min(rows, cols) // 2)
	cv2.circle(shadow_overlay, shadow_center, shadow_radius, (0, 0, 0), -1)
	shadow_img = cv2.addWeighted(img, 1 - shadow_intensity, shadow_overlay, shadow_intensity, 0)

	return shadow_img


def synthetizer(img_path, num_images=10):
	# Load image
	img = cv2.imread(img_path)

	for _ in range(num_images):
		# Randomly adjust brightness, contrast, and shadow intensity
		brightness_factor = random.uniform(0.5, 1.5)
		contrast_factor = random.uniform(0.5, 1.5)
		shadow_intensity = random.uniform(0.2, 0.5)

		# Add synthetic lighting effect
		synthetized_img = lighting_effect(img, brightness=brightness_factor, contrast=contrast_factor, shadow_intensity=shadow_intensity)

		# Yield sythetized image
		yield synthetized_img

		
image_path = os.path.join(src_dir, 'sample.jpg')
# TODO: check if path exists ...
print(image_path)
generator = synthetizer(image_path, num_images=10)

for i, img in enumerate(generator):
	output_path = os.path.join(dst_dir, f"synthetic_image_{i}.jpg")
	cv2.imwrite(output_path, img)