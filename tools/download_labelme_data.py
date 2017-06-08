import os
import glob
import shutil
from urllib2 import urlopen
import re

labelmeBaseFolder = 'data/labelme'
labelmeImageFolder = labelmeBaseFolder + '/Images'
labelmeAnnotationFolder = labelmeBaseFolder + '/Annotations'

labelmeBaseUrl = 'https://labelme.jz-c.org'
labelmeAnnotationBaseUrl = labelmeBaseUrl + '/' + 'Annotations'
labelmeImageBaseUrl = labelmeBaseUrl + '/' + 'Images'
labelmeCollections = ['flickr_yang', 'flickr_chris', 'flickr_jasper']

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

    print(filelist)

    for filename in filelist:
        # download annotation file
        annotationFilename = filename

        if not annotationFilename in alreadyDownloadedAnnotations:
            remoteAnnotationFile = urlopen(labelmeAnnotationBaseUrl + '/' + collection + '/' + annotationFilename)
            localAnnotationFile = open(labelmeAnnotationFolder + '/' + filename,'wb')
            localAnnotationFile.write(remoteAnnotationFile.read())
            localAnnotationFile.close()
            remoteAnnotationFile.close()

            print('download annotation: ' + annotationFilename)
        else:
            print('skip annotation: ' + annotationFilename)

        # download image file
        imageFilename = filename.replace('.xml', '.jpg')

        if not imageFilename in alreadyDownloadedImages:
            remoteImageFile = urlopen(labelmeImageBaseUrl + '/' + collection + '/' + imageFilename)
            localImageFile = open(labelmeImageFolder + '/' + imageFilename,'wb')
            localImageFile.write(remoteImageFile.read())
            localImageFile.close()
            remoteImageFile.close()

            print('download image: ' + imageFilename)
        else:
            print('skip image: ' + imageFilename)
