from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import argparse
import sys
import os
import numpy as np

def parse_args():
	parser = argparse.ArgumentParser(description='split data into train, val, test')
	parser.add_argument('--dataset_dir', dest='dataset_dir', help='Root directory to raw CVHCI dataset', default='data/CVHCI')
	parser.add_argument('--output_dir', dest='output_dir', help='Directory to save sets to', default='data/CVHCI/ImageSets')
	args = parser.parse_args()
	
	return args

if __name__ == '__main__':
	args = parse_args()

	in_dir = args.dataset_dir
	out_dir = args.output_dir
	cvhci_annotations = os.path.join(in_dir, 'Annotations')
	
	if not os.path.exists(in_dir):
		print('Path ' + in_dir + ' does not exist!')
		exit()
	
	if not os.path.exists(os.path.dirname(out_dir)):
		print('Path ' + os.path.dirname(out_dir) + ' does not exist!')
		exit()
	else:
		if not os.path.exists(out_dir):
			os.makedirs(out_dir)
			

	files = [f for f in os.listdir(cvhci_annotations) if os.path.isfile(os.path.join(cvhci_annotations, f))]
	np.random.shuffle(files)
	
	num_test = int(len(files) / 5)
	num_trainval = len(files) - num_test
	num_val = int(num_trainval / 5)
	num_train = num_trainval - num_val

	file_indices = [os.path.splitext(f)[0] for f in files]

	train, val, trainval, test = file_indices[:num_train], file_indices[num_train:num_train+num_val],\
								 file_indices[:num_train+num_val], file_indices[-num_test:]

	with open(os.path.join(out_dir, 'train.txt'), 'w') as fp:
		for x in train:
			fp.write(x + '\n')
	with open(os.path.join(out_dir, 'val.txt'), 'w') as fp:
		for x in val:
			fp.write(x + '\n')
	with open(os.path.join(out_dir, 'trainval.txt'), 'w') as fp:
		for x in trainval:
			fp.write(x + '\n')
	with open(os.path.join(out_dir, 'test.txt'), 'w') as fp:
		for x in test:
			fp.write(x + '\n')





