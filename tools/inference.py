import os
import mmcv
from mmcv.runner import load_checkpoint
from mmrotate.apis import inference_detector_by_patches
from mmdet.apis import inference_detector, show_result_pyplot
from mmrotate.models import build_detector
import xml.etree.ElementTree as ET
import math


# Set the root directory for the images and results
root_img_dir = '/home/jim.vanoosten/tinyfair1m/excasat/test/images'
root_res_dir = '/home/jim.vanoosten/JimageNet_results/test'

# Choose to use a config and initialize the detector
config = '/home/jim.vanoosten/mmrotate-OE/work_dirs_old/oe_net_687/oe_net.py'
config_name = os.path.splitext(os.path.basename(config))[0]

# Setup a checkpoint file to load
checkpoint = '/home/jim.vanoosten/mmrotate-OE/work_dirs_old/oe_net_687/epoch_12.pth'

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
# for img in os.listdir(root_img_dir):
img_name = '/home/jim.vanoosten/tinydota/test/images/P0170__1__942___0.png'
img_path = os.path.join(root_img_dir, img_name)
result = inference_detector_by_patches(model, img_name, [1024], [512], [1.0], 0.1)

# Save the result image to the output directory
output_file = '/home/jim.vanoosten/test2.png'
show_result_pyplot(model, img_path, result, score_thr=0.9, out_file=output_file) #palette='dota'
print(f"Result saved to {output_file}")

# Increment image_id
image_id += 1

# Single image 1024 patch
# img_name = '/home/jim.vanoosten/crazy_carpark.png'
# result = inference_detector(model, img_name)
# show_result_pyplot(model, img_name, result, score_thr=0.3, palette='dota', out_file='test1.png')

# Single image 512 patch
# img = '/home/jim.vanoosten/test4.png'
# result = inference_detector_by_patches(model, img, [512], [412], [1.0], 0.1)
# show_result_pyplot(model, img, result, score_thr=0.3, palette='dota', out_file='test4_result.png')






