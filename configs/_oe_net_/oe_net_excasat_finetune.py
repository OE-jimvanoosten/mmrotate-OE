_base_ = [
    '../_base_/datasets/excasat_1class_finetune.py', '../_base_/schedules/schedule_3x.py',
    '../_base_/default_runtime.py'
]

load_from = '/home/jim.vanoosten/mmrotate-OE/work_dirs/oe_net_excasat_fair/best_mAP_epoch_36.pth'
fp16 = dict(loss_scale='dynamic')
angle_version = 'le90'
model = dict(
    type='OrientedRCNN',

    # BACKBONE
    backbone=dict(
        type='ResNet',
        depth=50,
        num_stages=4,
        out_indices=(0, 1, 2, 3),
        frozen_stages=1,
        norm_cfg=dict(type='BN', requires_grad=True),
        norm_eval=True,
        style='pytorch',
        
        # oe-net adds a ContextBlock after the first conv layer
        plugins=[
            dict(
                cfg=dict(type='ContextBlock', ratio=0.25),
                position='after_conv1'),
        ],

        init_cfg=dict(type='Pretrained', checkpoint='torchvision://resnet50')),
    
    # NECK
    # oe-net uses DF-FPN instead of FPN
    neck=dict(
        type='DF_FPN', 
        in_channels=[256, 512, 1024, 2048],
        out_channels=256,
        num_outs=5),

    # PROPOSAL HEAD
    rpn_head=dict(
        type='BRAOrientedRPNHead',
        in_channels=256,
        feat_channels=256,
        version=angle_version,
        anchor_generator=dict(
            type='AnchorGenerator',
            scales=[8],
            ratios=[0.5, 1.0, 2.0],
            strides=[4, 8, 16, 32, 64]),
        bbox_coder=dict(
            type='MidpointOffsetCoder',
            angle_range=angle_version,
            target_means=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            target_stds=[1.0, 1.0, 1.0, 1.0, 0.5, 0.5]),
        loss_cls=dict(
            type='CrossEntropyLoss', use_sigmoid=True, loss_weight=1.0),
        loss_bbox=dict(
            type='SmoothL1Loss', beta=0.1111111111111111, loss_weight=1.0)),
    
    # DETECTION HEAD
    roi_head=dict(
        type='OrientedStandardRoIHead',
        bbox_roi_extractor=dict(
            type='RotatedSingleRoIExtractor',
            roi_layer=dict(
                type='RoIAlignRotated',
                out_size=7,
                sample_num=2,
                clockwise=True),
            out_channels=256,
            featmap_strides=[4, 8, 16, 32]),
        
        # oe-net uses VM_RotatedShared2FCBBoxHead instead of RotatedShared2FCBBoxHead
        bbox_head=dict(
            type='VM_RotatedShared2FCBBoxHead',
            in_channels=256,
            fc_out_channels=1024,
            roi_feat_size=7,
            num_classes=1,
            save_path='/home/jim.vanoosten/mmrotate-OE/configs/_oe_net_/vectors_excasat_1class.npy', # make sure to choose the path to the pretrained vectors here
            bbox_coder=dict(
                type='DeltaXYWHAOBBoxCoder',
                angle_range=angle_version,
                norm_factor=None,
                edge_swap=True,
                proj_xy=True,
                target_means=(.0, .0, .0, .0, .0),
                target_stds=(0.1, 0.1, 0.2, 0.2, 0.1)),
            reg_class_agnostic=True,
            loss_cls=dict(
                type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0),
            loss_bbox=dict(type='SmoothL1Loss', beta=1.0, loss_weight=1.0))),
    
    # TRAINING CONFIG
    train_cfg=dict(
        # oe-net uses RankingAssigner instead of MaxIoUAssigner
        rpn=dict(
            assigner=dict(
                type='BalancedRankingAssigner',
                ignore_iof_thr=-1,
                gpu_assign_thr=1200, 
                iou_calculator=dict(type='BboxDistanceMetric'),
                assign_metric='nwd',
                topk=2,
                alpha=6),
            sampler=dict(
                type='RandomSampler',
                num=256,
                pos_fraction=0.5,
                neg_pos_ub=-1,
                add_gt_as_proposals=False),
            allowed_border=0,
            pos_weight=-1,
            debug=False),
        rpn_proposal=dict(
            nms_pre=3000, 
            max_per_img=3000, 
            nms=dict(type='nms', iou_threshold=0.7), 
            min_bbox_size=0),
        rcnn=dict(
            assigner=dict(
                type='MaxIoUAssigner',
                pos_iou_thr=0.5,
                neg_iou_thr=0.5,
                min_pos_iou=0.5,
                match_low_quality=False,
                iou_calculator=dict(type='RBboxOverlaps2D'),
                ignore_iof_thr=-1,
                gpu_assign_thr=1200), 
            sampler=dict(
                type='RRandomSampler',
                num=512,
                pos_fraction=0.25,
                neg_pos_ub=-1,
                add_gt_as_proposals=True),
            pos_weight=-1,
            debug=False)),
    
    # TESTING CONFIG
    test_cfg=dict(
        rpn=dict(
            nms_pre=3000, 
            max_per_img=3000, 
            nms=dict(type='nms', iou_threshold=0.7), 
            min_bbox_size=0),
        rcnn=dict(
            nms_pre=3000,
            min_bbox_size=0,
            score_thr=0.05,
            nms=dict(iou_thr=0.5), 
            max_per_img=3000))) 

# DATASET CONFIG
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='RResize', img_scale=(1024, 1024)),
    dict(
        type='RRandomFlip',
        flip_ratio=[0.25, 0.25, 0.25],
        direction=['horizontal', 'vertical', 'diagonal'],
        version=angle_version),

    # oe-net uses PolyRandomRotate like LSKNet
    dict(
        type='PolyRandomRotate',
        rotate_ratio=0.5,
        angles_range=180,
        auto_bound=False,
        version=angle_version),

    dict(type='Normalize', **img_norm_cfg),
    dict(type='Pad', size_divisor=32),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels'])
]

data = dict(
    train=dict(pipeline=train_pipeline, version=angle_version),
    val=dict(version=angle_version),
    test=dict(version=angle_version))

# OPTIMIZER CONFIG
# oe-net uses AdamW optimizer instead of SGD
optimizer = dict(
    _delete_=True,
    type='AdamW',
    lr=0.000001, 
    betas=(0.9, 0.999),
    weight_decay=0.05)

evaluation = dict(interval=1, metric='mAP', save_best='mAP')
checkpoint_config = dict(interval=1, create_symlink=False)