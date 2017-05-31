import math
import glob
import xml.etree.ElementTree as et
from PIL import Image, ImageDraw

class Polygon:
	def __init__(self):
		self.points = []

	def addPoint(self, point):
		self.points.append(point)

	def toString(self):
		result = ''

		for point in self.points:
			result += point + ', '
		
		return result

"""
Class to create a bounding box of a given polygon.
The corners of the box are saved in the class variables p1 and p2. 
"""
class BoundingBox:
	def __init__(self, polygon):
		min_x = polygon.points[0][0]
		min_y = polygon.points[0][1]
		max_x = polygon.points[0][0]
		max_y = polygon.points[0][1]

		for point in polygon.points:
			min_x = min(min_x, point[0])
			min_y = min(min_y, point[1])
			max_x = max(max_x, point[0])
			max_y = max(max_y, point[1])

		self.p1 = (min_x, min_y)
		self.p2 = (max_x, max_y)

"""
Class to save the annotations as a list of polygons and the filename of the associated image.
"""
class ImageAnnotation:
	def __init__(self, image_filename, polygons):
		self.image_filename = image_filename
		self.polygons = polygons

"""
Class to extract annotations from xml-files created by the LabelMe tool.
"""
class LabelMe:
	"""
	Method to create a class object for the given image and annotation directory
	"""
	def __init__(self, images_dir, annotations_dir):
		self.images_dir = images_dir
		self.annotations_dir = annotations_dir

	"""
	Extracts all annotations from the annotation directory and saves them in a list of annotation objects
	"""
	def extractImageAnnotations(self):
		imageAnnotations = []
		annotation_paths = glob.glob(self.annotations_dir + '/*.xml')


		for annotation_path in annotation_paths:
			xml_tree = et.parse(annotation_path)
			xml_root = xml_tree.getroot()
			xml_polygons = xml_root.findall("./object/polygon")
			polygons = []
			image_filename = xml_root.find('filename').text

			if len(xml_polygons) > 0:
				for xml_polygon in xml_polygons:
					polygon = Polygon()
					points = xml_polygon.iter('pt')

					for point in points:
						x = int(point.find('x').text)
						y = int(point.find('y').text)

						polygon.addPoint((x, y))

					polygons.append(polygon)

			imageAnnotations.append(ImageAnnotation(image_filename, polygons))

		return imageAnnotations

def calcBoundingBoxImageRatio(boundingBox, image):
	# calculate bounding box size
	boundingBoxSize = abs((boundingBox.p1[0] - boundingBox.p2[0]) * (boundingBox.p1[1] - boundingBox.p2[1]))
	# calculate image size
	imageSize = image.size[0] * image.size[1]
	# calculate ratio between image and bounding box size

	return boundingBoxSize * 1.0 / imageSize * 1.0

def calcPolygonArea(polygon):
	n = len(polygon.points)

	if n < 3: 
		return 0.0

	a = 0.0
	points = polygon.points

	for i in range(0, n):
		a += (points[i][1] + points[(i+1) % n][1]) * (points[i][0] - points[(i+1) % n][0]);

	return abs(a / 2.0)

def calcPolygonBoundingBoxRatio(polygon, boundingBox):
	# calculate bounding box size
	boundingBoxSize = abs((boundingBox.p1[0] - boundingBox.p2[0]) * (boundingBox.p1[1] - boundingBox.p2[1]))
	# calculate area of polygon
	polygonSize = calcPolygonArea(polygon)

	return polygonSize * 1.0 / boundingBoxSize * 1.0
	

images_dir = './Images'
annotations_dir = './Annotations'
out_dir = './Out'

labelMe = LabelMe(images_dir, annotations_dir)
imageAnnotations = labelMe.extractImageAnnotations()

stats = []
for i in range(0, 100):
	stats.append(0)

for annotation in imageAnnotations:
	image = Image.open(images_dir + '/' + annotation.image_filename).convert('RGB')
	image_drawing = ImageDraw.Draw(image, mode='RGB')
	saveImage = False

	print(annotation.image_filename)

	if len(annotation.polygons) == 1:
		for polygon in annotation.polygons:
			if len(polygon.points) > 1:
				# draw polygon
				for i in range(1, len(polygon.points)):
					image_drawing.line([polygon.points[i - 1], polygon.points[i]], fill=(34, 255, 0), width=4)

				image_drawing.line([polygon.points[len(polygon.points) - 1], polygon.points[0]], fill=(34, 255, 0), width=4)

				# draw bounding box
				boundingBox = BoundingBox(polygon);
				image_drawing.line([boundingBox.p1, (boundingBox.p1[0], boundingBox.p2[1])], fill=(0, 0, 255), width=4)
				image_drawing.line([(boundingBox.p1[0], boundingBox.p2[1]), boundingBox.p2], fill=(0, 0, 255), width=4)
				image_drawing.line([boundingBox.p2, (boundingBox.p2[0], boundingBox.p1[1])], fill=(0, 0, 255), width=4)
				image_drawing.line([(boundingBox.p2[0], boundingBox.p1[1]), boundingBox.p1], fill=(0, 0, 255), width=4)

				#ratio = calcBoundingBoxImageRatio(boundingBox, image)
				ratio = calcPolygonBoundingBoxRatio(polygon, boundingBox)

				# save image only if the ratio between the bounding box and the image size is under a specified threshold
				#if ratio < 0.25:
				#	saveImage = True

				stats[int(math.floor(ratio * 100.0))] += 1

	if saveImage == True:
		image.save(out_dir + '/' + annotation.image_filename)

for i in range(0, 100):
	print(str(i) + ": " + str(stats[i]))

