from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import cv2

# Initialize COCO api for instance annotations
coco = COCO('annotations/instances_train2017.json')

# Load the image with the specified ID
image_id = 473870
image_info = coco.loadImgs(image_id)[0]
image_path = 'train2017/' + image_info['file_name']
image = io.imread(image_path)

# Load the annotations for the specified image
ann_ids = coco.getAnnIds(imgIds=image_id, iscrowd=False)
anns = coco.loadAnns(ann_ids)

# Create a mask for the person category (category_id=1)
person_mask = np.zeros((image_info['height'], image_info['width']))
for ann in anns:
    if ann['category_id'] == 1:
        person_mask = np.maximum(person_mask, coco.annToMask(ann))

# Apply the mask to the image to remove the background
person_image = cv2.bitwise_and(image, image, mask=person_mask.astype(np.uint8))

# Save and display the result
output_path = 'person_only.png'
cv2.imwrite(output_path, cv2.cvtColor(person_image, cv2.COLOR_RGB2BGR))
plt.imshow(person_image)
plt.axis('off')
plt.show()

print(f"The image with ID {image_id} has been processed and saved as {output_path}.")
