<div align="center">
  <img src="mmrotate-OE/resources/excavator.png" width="400">
</div>

## Installation

MMRotate depends on [PyTorch](https://pytorch.org/), [MMCV](https://github.com/open-mmlab/mmcv) and [MMDetection](https://github.com/open-mmlab/mmdetection).
Below are quick steps for installation.
Please refer to [Install Guide](https://mmrotate.readthedocs.io/en/latest/install.html) for more detailed instruction.

### Get conda

```shell
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
```

### Create new shell and run

```shell
conda create -n hrod python=3.7 -y
conda activate hrod
conda install pytorch==1.8.0 torchvision==0.9.0 torchaudio==0.8.0 cudatoolkit=11.1 -c pytorch -c conda-forge
pip install openmim
mim install mmcv-full==1.6.1
mim install mmdet==2.25.1
git clone https://github.com/OE-jimvanoosten/mmrotate-OE.git
cd mmrotate-OE
pip install -r requirements/build.txt
pip install -v -e .
pip install timm apex yapf==0.40.1
```

## Get Started

### Train OE-Net

```shell
python tools/train.py mmrotate-OE/configs/_oe_net_/oe_net.py
```

### Test OE-Net

```shell
python tools/test.py mmrotate-OE/configs/_oe_net_/oe_net.py path/to/model/weights.pth
```