#!/usr/bin/env python

# --------------------------------------------------------
# Tensorflow Faster R-CNN
# Licensed under The MIT License [see LICENSE for details]
# Written by Xinlei Chen, based on code from Ross Girshick
# --------------------------------------------------------

"""
Demo script showing detections in sample images.

See README.md for installation instructions before running.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

#import _init_paths
from lib.model.config import cfg
from lib.model.test import im_detect
from lib.model.nms_wrapper import nms

from lib.utils.timer import Timer
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import os, cv2
import argparse
import glob

from nets.vgg16 import vgg16
from nets.resnet_v1 import resnetv1

CLASSES = ('__background__', 'stairs')

NETS = {'vgg16': ('vgg16_faster_rcnn_iter_30000.ckpt',),'res101': ('res101_faster_rcnn_iter_110000.ckpt',)}
DATASETS= {'pascal_voc': ('voc_2007_trainval',),'pascal_voc_0712': ('voc_2007_trainval+voc_2012_trainval',), 'stairs': ('stairs_trainval')}

def vis_detections(im, class_name, dets, thresh=0.5):
    """Draw detected bounding boxes."""
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return

    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]

        cv2.rectangle(im, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 3)
        cv2.putText(im, '{:s} {:.3f}'.format(class_name, score), (int(bbox[0]), int(bbox[1] - 2)), cv2.FONT_HERSHEY_SIMPLEX,  1, (255, 255, 255), 2)
    
    return im

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Tensorflow Faster R-CNN stairs_demo')
    parser.add_argument('--net', dest='demo_net', help='Network to use [vgg16 res101]',
                        choices=NETS.keys(), default='vgg16')
    parser.add_argument('--dataset', dest='dataset', help='Trained dataset [pascal_voc pascal_voc_0712 stairs]',
                        choices=DATASETS.keys(), default='stairs')
    parser.add_argument('--video', dest='video_path', help='Path to the video file', required=True)
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    cfg.TEST.HAS_RPN = True  # Use RPN for proposals
    args = parse_args()

    # model path
    demonet = args.demo_net
    dataset = args.dataset
    print('demonet: ' + demonet)
    print('test: ' + DATASETS[dataset])
    tfmodel = os.path.join('output', demonet, DATASETS[dataset], 'default',
                              NETS[demonet][0])
    print('tfmodel: ' + tfmodel)

    if not os.path.isfile(tfmodel + '.meta'):
        raise IOError(('{:s} not found.\nDid you download the proper networks from '
                       'our server and place them properly?').format(tfmodel + '.meta'))

    # set config
    tfconfig = tf.ConfigProto(allow_soft_placement=True)
    tfconfig.gpu_options.allow_growth=True
	
    # init session
    sess = tf.Session(config=tfconfig)
    # load network
    if demonet == 'vgg16':
        net = vgg16(batch_size=1)
    elif demonet == 'res101':
        net = resnetv1(batch_size=1, num_layers=101)
    else:
        raise NotImplementedError
    
    # the parameter with value 2 is the number of classes
    net.create_architecture(sess, "TEST", 2, tag='default', anchor_scales=[4, 8, 16, 32])
    saver = tf.train.Saver()
    saver.restore(sess, tfmodel)

    print('Loaded network {:s}'.format(tfmodel))

    cap = cv2.VideoCapture(args.video_path)
    length = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    i = 0
    
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    out = cv2.VideoWriter('/tmp/output.avi', fourcc, fps / 5, (640,480))
    
    def onChange(trackbarValue):
        cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, trackbarValue)
        err,img = cap.read()
        cv2.imshow("stair detection", img)
        pass
    
    cv2.namedWindow('stair detection')
    cv2.createTrackbar( 'frame', 'stair detection', 0, length, onChange)
    
    onChange(i)
    cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, i)
    
    while(cap.isOpened()):
		ret, frame = cap.read()
		
		if i % 5 == 0:
			cv2.setTrackbarPos('frame', 'stair detection', int(cap.get(1)))
			"""Detect object classes in an image using pre-computed object proposals."""
			
			copy = frame.copy()
			frame = cv2.resize(copy, (640,480)) 

			# Detect all object classes and regress object bounds
			timer = Timer()
			timer.tic()
			scores, boxes = im_detect(sess, net, frame)
			timer.toc()
			print('Detection took {:.3f}s for {:d} object proposals'.format(timer.total_time, boxes.shape[0]))

			# Visualize detections for each class
			CONF_THRESH = 0.8
			NMS_THRESH = 0.3
			
			for cls_ind, cls in enumerate(CLASSES[1:]):
				cls_ind += 1 # because we skipped background
				cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
				cls_scores = scores[:, cls_ind]
				dets = np.hstack((cls_boxes,
				                  cls_scores[:, np.newaxis])).astype(np.float32)
				keep = nms(dets, NMS_THRESH)
				dets = dets[keep, :]
				vis_detections(frame, cls, dets, thresh=CONF_THRESH)
				
			out.write(frame)

			cv2.imshow('stair detection',frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		
		i += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    plt.show()
