import os
import glob
import shutil
from urllib2 import urlopen
import re
import argparse
import urlparse

def parse_args():
	parser = argparse.ArgumentParser(description='Downloader to fetch CVHCI dataset from a LabelMe instance')
	parser.add_argument('--labelme_url', dest='labelme_url', help='Base URL for the LabelMe web interface', default='https://labelme.jz-c.org')
	parser.add_argument('--labelme_collections', dest='labelme_collections', help='Collections to fetch seperated by ","', default='flickr_yang,flickr_chris,flickr_jasper')
	parser.add_argument('--output_path', dest='output_path', help='Path to save CVHCI dataset', default='data/CVHCI')
	args = parser.parse_args()

	return args

if __name__ == '__main__':
	args = parse_args()

	labelmeBaseUrl = args.labelme_url
	labelmeCollections = args.labelme_collections.split(',')
	labelmeAnnotationBaseUrl = urlparse.urljoin(labelmeBaseUrl, 'Annotations')
	labelmeImageBaseUrl = urlparse.urljoin(labelmeBaseUrl, 'Images')

	labelmeBaseFolder = args.output_path
	labelmeImageFolder = os.path.join(labelmeBaseFolder, 'Images')
	labelmeAnnotationFolder = os.path.join(labelmeBaseFolder, 'Annotations')

	# create folder structure for pascal voc format with the two folders Annotations ans JPEGImages
	if not os.path.exists(labelmeBaseFolder):
		os.makedirs(labelmeBaseFolder)

	if not os.path.exists(labelmeImageFolder):
		os.makedirs(labelmeImageFolder)

	if not os.path.exists(labelmeAnnotationFolder):
		os.makedirs(labelmeAnnotationFolder)

	alreadyDownloadedAnnotationPaths = str(glob.glob(labelmeAnnotationFolder + '/*.xml'))
	alreadyDownloadedImagePaths = str(glob.glob(labelmeImageFolder + '/*.jpg'))

	annotationPattern = re.compile('[a-z0-9]*\_[a-z0-9]*\_[a-z]*.xml')
	imagePattern = re.compile('[a-z0-9]*\_[a-z0-9]*\_[a-z]*.jpg')

	alreadyDownloadedAnnotations = annotationPattern.findall(alreadyDownloadedAnnotationPaths)
	alreadyDownloadedImages = imagePattern.findall(alreadyDownloadedImagePaths)

	for collection in labelmeCollections:
		urlpath =urlopen(labelmeAnnotationBaseUrl + '/' + collection)
		string = urlpath.read().decode('utf-8')

		filelist = list(set(annotationPattern.findall(string)))

		for filename in filelist:
			# download annotation file
			annotationFilename = filename

			if not annotationFilename in alreadyDownloadedAnnotations:
				remoteAnnotationFile = urlopen(labelmeAnnotationBaseUrl + '/' + collection + '/' + annotationFilename)
				localAnnotationFile = open(labelmeAnnotationFolder + '/' + filename,'wb')
				localAnnotationFile.write(remoteAnnotationFile.read())
				localAnnotationFile.close()
				remoteAnnotationFile.close()

			#	print('download annotation: ' + annotationFilename)
			#else:
			#	print('skip annotation: ' + annotationFilename)

			# download image file
			imageFilename = filename.replace('.xml', '.jpg')

			if not imageFilename in alreadyDownloadedImages:
				remoteImageFile = urlopen(labelmeImageBaseUrl + '/' + collection + '/' + imageFilename)
				localImageFile = open(labelmeImageFolder + '/' + imageFilename,'wb')
				localImageFile.write(remoteImageFile.read())
				localImageFile.close()
				remoteImageFile.close()

			#	print('download image: ' + imageFilename)
			#else:
			#	print('skip image: ' + imageFilename)
