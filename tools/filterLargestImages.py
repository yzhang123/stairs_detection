import argparse
import os
import sys
from collections import defaultdict
import operator
import re

"""
usage example:
python filterLargestImages.py --input ../urls/escalator/pages ../urls/steps/pages   --output pages_unique
"""

def parseFile(f, d):
    """
    parses file and adds its elements to the given dictionary

    :@param f: file
    :@param d: defaultdictionary
    :raises Error if a line in the file f does not have 3 segments divided by white space

    """
    with open(f, 'r') as fp:
        for line in fp.readlines():
            list = line.split()
            assert(len(list)==3), "wrong format: expected img_name width height"
            img_name = list[0].strip()
            img_key = re.split("(_[a-z])?.jpg", img_name)[0]
            #print("img_key : %s " % img_key)
            if img_key not in d:
                print("img_key : %s " % img_key)
            if img_name not in d[img_key]:
                #print("img_name : %s " % img_name)
                width = int(list[1].split(':')[1].strip())
                height = int(list[2].split(':')[1].strip())
                area = width * height
                d[img_key][img_name] = area

def filterLargestFiles(d):
    """
    returns the image names with the largest image size

    :param d: dictionary containing the images and their sizes
    :return list of images names where the corresponding image has the largest size/area
    """
    return [max(x.iteritems(), key=operator.itemgetter(1))[0] for x in d.values()]




def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help='image urls', metavar='N', nargs='+')
    parser.add_argument("--output", type=str, help='output file')
    return parser.parse_args()

if __name__=='__main__':
    args = parse()
    d = defaultdict(defaultdict)
    in_files = args.input
    out_file = args.output

    for file in in_files:
        parseFile(file, d)

    l_images = filterLargestFiles(d)
    with open(out_file, 'w') as fp:
        for img in l_images:
            fp.write(img+"\n")




    
