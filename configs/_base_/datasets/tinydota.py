# dataset settings
dataset_type = 'DOTAtinyDataset'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='RResize', img_scale=(1024, 1024)),
    dict(type='RRandomFlip', flip_ratio=0.5),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='Pad', size_divisor=32),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels'],meta_keys=('img_shape'))
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(1024, 1024),
        flip=False,
        transforms=[
            dict(type='RResize'),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='Pad', size_divisor=32),
            dict(type='DefaultFormatBundle'),
            dict(type='Collect', keys=['img'])
        ])
]
data = dict(
    samples_per_gpu=4,
    workers_per_gpu=4,
    train=dict(
        type=dataset_type,
        ann_file='/home/jim.vanoosten/tinydota/train/labelTxt/',
        img_prefix='/home/jim.vanoosten/tinydota/train/images/',
        pipeline=train_pipeline),
    val=dict(
        type=dataset_type,
        ann_file='/home/jim.vanoosten/tinydota/val/labelTxt/',
        img_prefix='/home/jim.vanoosten/tinydota/val/images/',
        pipeline=test_pipeline),
    test=dict(
        type=dataset_type,
        ann_file='/home/jim.vanoosten/tinydota/test/labelTxt/',
        img_prefix='/home/jim.vanoosten/tinydota/test/images/',
        pipeline=test_pipeline))