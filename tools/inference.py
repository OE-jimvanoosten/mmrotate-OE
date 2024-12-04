# Turn into a tools/inference.py file which you can run from the command line and give
# arguments to. This script should be able to take in a config file, a checkpoint file, a data root
# and an output root. It should then run inference on the data root and save the results to the output

import os
import mmcv
from mmcv.runner import load_checkpoint
from mmrotate.apis import inference_detector_by_patches
from mmdet.apis import inference_detector, show_result_pyplot
from mmrotate.models import build_detector
import xml.etree.ElementTree as ET
import math

# Define the label mapping for your dataset
LABELS = {
    0: 'plane',
    1: 'bridge',
    2: 'small-vehicle',
    3: 'large-vehicle',
    4: 'ship',
    5: 'storage-tank',
    6: 'swimming-pool',
    7: 'helicopter'
}

# Define the allowed classes you want to keep
ALLOWED_CLASSES = ['small-vehicle', 'large-vehicle']

def append_results_to_cvat_xml(tree, result, image_name, image_id, width, height, threshold=0.3):
    """Appends results of a single image to an existing XML tree."""
    # Get the root of the tree
    annotations = tree.getroot()

    # Add image node
    image_node = ET.SubElement(annotations, "image", {
        "id": str(image_id),
        "name": image_name,
        "width": str(width),
        "height": str(height),
        "task_id": "878716",  # Adjust task ID if necessary
    })

    # Loop over the results (list of arrays per class)
    for class_index, boxes in enumerate(result):
        label_name = LABELS.get(class_index, 'unknown')  # Get label name from index

        # Only process if the class is either 'small-vehicle' or 'large-vehicle'
        if label_name not in ALLOWED_CLASSES:
            continue

        # Process each bounding box
        for box in boxes:
            x_center, y_center, width, height, angle, score = box

            # Apply threshold filtering
            if score < threshold:
                continue

            # Convert radians to degrees for CVAT and ensure positive angle
            rotation_degrees = math.degrees(angle)
            if rotation_degrees < 0:
                rotation_degrees += 360  # Ensure non-negative rotation

            # Calculate the corners of the bounding box
            xtl = x_center - (width / 2)
            ytl = y_center - (height / 2)
            xbr = x_center + (width / 2)
            ybr = y_center + (height / 2)

            # Add box element
            box_node = ET.SubElement(image_node, "box", {
                "label": label_name,
                "occluded": "0",
                "xtl": str(xtl),
                "ytl": str(ytl),
                "xbr": str(xbr),
                "ybr": str(ybr),
                "rotation": str(rotation_degrees),
                "z_order": "0"
            })

# Set the root directory for the images and results
root_img_dir = '/home/jim.vanoosten/tinydota/test/images'
root_res_dir = '/home/jim.vanoosten/JimageNet_results'

# Choose to use a config and initialize the detector
config = '/home/jim.vanoosten/mmrotate-OE/work_dirs/oe_net_687/oe_net.py'
config_name = os.path.splitext(os.path.basename(config))[0]

# Setup a checkpoint file to load
checkpoint = '/home/jim.vanoosten/mmrotate-OE/work_dirs/oe_net_687/epoch_12.pth'

# create folder inside inference results folder with config_name as name
newpath = os.path.join(root_res_dir, config_name)
if not os.path.exists(newpath):
    os.makedirs(newpath)

# Set the device to be used for evaluation
device = 'cuda:0'

# Load the config
config = mmcv.Config.fromfile(config)

# Set pretrained to be None since we do not need pretrained model here
config.model.pretrained = None

# Initialize the detector
model = build_detector(config.model)

# Load checkpoint
checkpoint = load_checkpoint(model, checkpoint, map_location=device)

# Set the classes of models for inference
model.CLASSES = checkpoint['meta']['CLASSES']

# We need to set the model's cfg for inference
model.cfg = config

# Convert the model to GPU
model.to(device)

# Convert the model into evaluation mode
model.eval()

# Initialize the XML tree with a root element
annotations = ET.Element("annotations")

# Add metadata (adjust this according to your needs)
meta = ET.SubElement(annotations, "meta")
ET.SubElement(meta, "project")
ET.SubElement(meta, "labels")

# Create an ElementTree object
tree = ET.ElementTree(annotations)

# Initiate image_id
image_id = 0

# Use the detector to do inference
for img in os.listdir(root_img_dir)[:500]:
    img_name = img
    img_path = os.path.join(root_img_dir, img)
    result = inference_detector_by_patches(model, img_path, [1024], [512], [1.0], 0.1)
    
    # Save the result image to the output directory
    output_file = os.path.join(newpath, img)
    show_result_pyplot(model, img_path, result, palette='dota', score_thr=0.4, out_file=output_file) #palette='dota'
    print(f"Result saved to {output_file}")
    
    # XML information
    width, height = 1024, 1024  # Adjust according to your image dimensions
    threshold = 0.4

    # Append the results to the existing XML tree
    # append_results_to_cvat_xml(tree, result, img_name, image_id, width, height, threshold)

    # Increment image_id
    image_id += 1

# Save the XML tree to a file (once, after all images are processed)
# xml_output_path = os.path.join(newpath, "output_annotations.xml")
# tree.write(xml_output_path, encoding="utf-8", xml_declaration=True)
# print(f"XML annotations saved to {xml_output_path}")

# Single image 1024 patch
# img_name = '/home/jim.vanoosten/crazy_carpark.png'
# result = inference_detector(model, img_name)
# show_result_pyplot(model, img_name, result, score_thr=0.3, palette='dota', out_file='test1.png')

# Single image 512 patch
# img = '/home/jim.vanoosten/test4.png'
# result = inference_detector_by_patches(model, img, [512], [412], [1.0], 0.1)
# show_result_pyplot(model, img, result, score_thr=0.3, palette='dota', out_file='test4_result.png')






