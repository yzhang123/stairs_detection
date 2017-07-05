import os
import glob
import argparse
import xml.etree.ElementTree as et
from lxml import etree

def parse_args():
	parser = argparse.ArgumentParser(description='Filter dataset for deleted polygons still present in xml annotation file and delete them')
	parser.add_argument('--dataset_dir', dest='dataset_dir', help='Root directory to raw CVHCI dataset', default='data/CVHCI')
	args = parser.parse_args()
	
	return args

if __name__ == '__main__':
	args = parse_args()
	
	data_dir = args.dataset_dir
	annotation_dir = os.path.join(data_dir, 'Annotations')
	annotation_paths = [os.path.join(annotation_dir, f) for f in os.listdir(annotation_dir) if os.path.isfile(os.path.join(annotation_dir, f))]
	
	for annotation_path in annotation_paths:
		doc = etree.parse(annotation_path)
		root = doc.getroot()
		objects = root.findall('object')
		
		for obj in objects:
			if int(obj.findtext('deleted')) == 1:
				root.remove(obj)
				
			if obj.findtext('name') == 'escalator':
				obj.find('name').text = 'stairs'
		
		objects_after = root.findall('object')
		
		if len(objects_after) > 0:
			new_doc = etree.ElementTree(root)
			new_doc.write(annotation_path, pretty_print=True)
		else:
			os.remove(annotation_path)

