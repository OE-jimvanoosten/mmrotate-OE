# GET_STARTED.md

This document is intended to help you understand and navigate the mmrotate-OE repository effectively. Below is a breakdown of the repository structure, workflow, and troubleshooting tips.

---

## Repository Structure

The `mmrotate-OE` repository consists of three primary folders:

### 1. **`configs`**

- Contains configuration files for models. OE-Net is in the `configs/_oe_net_/` folder. The config files for your datasets (paths, preprocessing settings, batch size, etc.) and your training schedules (optimizer config, validation settings, etc.) are stored in the `configs/_base_/datasets/` and the ` configs/_base_/schedules/` folders, respectively.

All in all, the config files define:

  - Model architecture.
  - Training parameters (e.g., learning rate, epochs).
  - Dataset paths and augmentation pipelines.

- Config files like `oe_net_excasat.py` inherit base configurations for datasets and training schedules, as can be seen in the first lines of the config file.

### 2. **`mmrotate`**

- Holds Python scripts that define the necessary classes for modules.
- Key components:
  - Custom datasets. In the `mmrotate/datasets/` folder, you store your script that makes sure the dataset (and especially the format of the images and the annotations) can be loaded and prepared for training/testing effectively. Make sure to add newly registered class to init file, if you introduce new dataset class!
  - Custom modules. In the `mmrotate/models/` folder, the custom modules are stored. These include necks, proposal heads, detection heads, and much more. OE-Net inherits most of its modules, from here (e.g. `mmrotate/models/dense_heads/bra_oriented_rpn_head.py` contains the BRAOrientedRPNHead.)
  - Core modules. In the `mmrotate/core/` folder, key modules such as the anchor generator, the assigner, the sampler, and the overlap calculator are given.
  - Models. In the `\mmrotate/models/detectors/` folder, the `oriented_rcnn.py` file contains the initializaztion for the model. Its parent class, `RotatedTwoStageDetector`, contains the forward train function that activates the modules in the detector. OE-Net is also an Oriented R-CNN model, but it uses a number different modules (indicated in OE-Net config file).
- **Registry System:** Classes/modules are registered in a registry system, such that when you train/test, and the model is built from your config, the builder can find the modules that you are mentioning in your config file.

### 3. **`tools`**

- Contains scripts to:
  - Train models (`train.py`).
  - Test models (`test.py`).
  - Perform inference (`inference.py`).
  - Prelabel images (`prelabeling.py`).
  - Annotation conversion (`label_conversion_cvat2dota.py`)

- Acts as the entry point for running training and evaluation tasks.

---

## Dependencies from External Repositories

### mmdetection

- Some modules in `mmrotate-OE` inherit from `mmdetection`, such as the ResNet-50 backbone. These classes are located in:
  `/home/jim.vanoosten/miniconda3/envs/hrod/lib/python3.7/site-packages/mmdet`

### mmcv

- Additional utilities and base classes are imported from `mmcv`. These are located in:
  `/home/jim.vanoosten/miniconda3/envs/hrod/lib/python3.7/site-packages/mmcv`

If a required class or module is not found in the `mmrotate` folder, check the above locations.

---

## Debugging & Searching for Classes

1. Use **VSCode’s Global Search**:

   - Press `Ctrl + Shift + F`.
   - Search for `class <CLASS_NAME>` to locate the definition of the class.

2. **Trace the Inheritance**:

   - Start with the configuration file.
   - Identify the classes/modules it imports.
   - Look for their definitions in `mmrotate`. If not found, check `mmdetection` or `mmcv`.

---

## Workflow Overview

### Training

1. **Entry Point:** `train.py`.

   - Requires the path to a config file.

2. **Config Processing:**

   - The script processes the config file by including all inherited base files, resulting in a unified configuration.

3. **Model Building:**

   - The builder checks the `mmrotate` registry for registered classes.
   - If a class is not found, it searches the `mmdetection` folder in the environment.

4. **DataLoader:**

   - The configuration triggers the dataloader to prepare the dataset for training.

5. **Epoch-Based Runner:**

   - The `EpochBasedRunner` begins executing the training loops.

### Testing

1. **Entry Point:** `test.py`.

   - Similar to `train.py`, requires a config file, but also a weights file.

2. **Hook Activation:**

   - Instead of starting training, a testing hook is triggered to evaluate the model.

---

## Additional Notes

- **Config Inheritance:**

  - Config files often rely on inheritance to streamline definitions. Ensure that all referenced base config files are accessible.

- **Registry:**

  - The registry in `mmrotate` ensures that custom classes are discoverable. If you add a new class, make sure it is registered properly.

- **Common Errors:**

  - **ClassNotFound:** Occurs if the class is not registered or if the module is not imported correctly.
  - **Path Issues:** Double-check dataset paths in config files to avoid `FileNotFound` errors.

---

This document provides a foundational understanding of the `mmrotate-OE` repository. For further assistance, Slack me!
