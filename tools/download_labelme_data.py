import os
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
if os.path.exists(labelmeBaseFolder):
    shutil.rmtree(labelmeBaseFolder)

os.makedirs(labelmeBaseFolder)
os.makedirs(labelmeImageFolder)
os.makedirs(labelmeAnnotationFolder)

for collection in labelmeCollections:
    urlpath =urlopen(labelmeAnnotationBaseUrl + '/' + collection)
    string = urlpath.read().decode('utf-8')

    pattern = re.compile('[a-z0-9]*\_[a-z0-9]*\_[a-z]*.xml') #the pattern actually creates duplicates in the list

    filelist = pattern.findall(string)

    for filename in filelist:
        # download annotation file
        annotationFilename = filename
        remoteAnnotationFile = urlopen(labelmeAnnotationBaseUrl + '/' + collection + '/' + annotationFilename)
        localAnnotationFile = open(labelmeAnnotationFolder + '/' + filename,'wb')
        localAnnotationFile.write(remoteAnnotationFile.read())
        localAnnotationFile.close()
        remoteAnnotationFile.close()

        # download image file
        imageFilename = filename.replace('.xml', '.jpg')
        remoteImageFile = urlopen(labelmeImageBaseUrl + '/' + collection + '/' + imageFilename)
        localImageFile = open(labelmeImageFolder + '/' + imageFilename,'wb')
        localImageFile.write(remoteImageFile.read())
        localImageFile.close()
        remoteImageFile.close()
