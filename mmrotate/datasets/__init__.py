# Copyright (c) OpenMMLab. All rights reserved.
from .builder import build_dataset  # noqa: F401, F403
from .dota import DOTADataset  # noqa: F401, F403
from .hrsc import HRSCDataset  # noqa: F401, F403
from .pipelines import *  # noqa: F401, F403
from .sar import SARDataset  # noqa: F401, F403
from .tinydota import DOTAtinyDataset
from .fair1m import FAIR1MDataset

__all__ = ['SARDataset', 'DOTADataset', 'build_dataset', 
           'HRSCDataset', 'DOTAtinyDataset', 'FAIR1MDataset']
