# GET_STARTED.md

This document is intended to help your successor understand and navigate the mmrotate-OE repository effectively. Below is a breakdown of the repository structure, workflow, and troubleshooting tips.

---

## Repository Structure

The `mmrotate-OE` repository consists of three primary folders:

### 1. **`configs`**

- Contains configuration files for various models.
- These files define:
  - Model architecture.
  - Training parameters (e.g., learning rate, epochs).
  - Dataset paths and augmentation pipelines.
- Config files often inherit base configurations to reduce duplication.

### 2. **`mmrotate`**

- Holds Python scripts that define the necessary classes for modules.
- Key components:
  - Custom datasets.
  - Custom models and heads.
  - Training hooks and utilities.
- **Registry System:** This folder registers classes used in the repository so they can be located during training/testing.

### 3. **`tools`**

- Contains scripts to:
  - Train models (`train.py`).
  - Test models (`test.py`).
  - Perform inference.
- Acts as the entry point for running training and evaluation tasks.

---

## Dependencies from External Repositories

### mmdetection

- Many classes in `mmrotate-OE` inherit from `mmdetection`. These classes are located in:
  `/home/jim.vanoosten/miniconda3/envs/hrod/lib/python3.7/site-packages/mmdet`

### mmcv

- Additional utilities and base classes are imported from `mmcv`. These are located in:
  `/home/jim.vanoosten/miniconda3/envs/hrod/lib/python3.7/site-packages/mmcv`

If a required class or module is not found in `mmrotate`, check the above locations.

---

## Debugging & Searching for Classes

1. Use **VSCode’s Global Search**:

   - Press `Ctrl + Shift + F`.
   - Search for `class <CLASS_NAME>` to locate the definition of the class.

2. **Trace the Inheritance**:

   - Start with the configuration file.
   - Identify the classes it imports.
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

   - Similar to `train.py`, requires a config file.

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

This document provides a foundational understanding of the `mmrotate-OE` repository. For further assistance, refer to specific scripts and documentation within the repository or reach out for clarification.
