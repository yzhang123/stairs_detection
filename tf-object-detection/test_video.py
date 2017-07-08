import sys
import os
sys.path.append(os.path.join(os.environ['PATH_TO_TENSORFLOW_MODEL_REPOSITORY'], 'object_detection'))

from utils import label_map_util
from utils import visualization_utils as vis_util
import numpy as np
import tensorflow as tf
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import argparse

PATH_TO_CKPT = 'inference_output/output_inference_graph.pb'
PATH_TO_LABELS = 'data/cvhci_label_map.pbtxt'
NUM_CLASSES = 1

CV_OUTPUT_WINDOW_NAME = 'Stair detection on video'
CV_FRAME_TRACKBAR_NAME = ' frame trackbar'

def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size

    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)

def parse_args():
	parser = argparse.ArgumentParser(description='Detect all stairs in a video file')
	parser.add_argument('--video_input', dest='video_input', help='Path to the video input file', required=True)
	parser.add_argument('--video_output', dest='video_output', help='Path to the video output file', required=True)
	parser.add_argument('--first_frame', dest='first_frame', help='Start frame to play the video', default=0)
	args = parser.parse_args()

	return args

def onChange(trackbarValue):
    cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, trackbarValue)
    err, img = cap.read()
    cv2.imshow(CV_OUTPUT_WINDOW_NAME, img)
    pass

if __name__ == '__main__':
    args = parse_args()

    video_input = args.video_input
    video_output = args.video_output
    first_frame = int(args.first_frame)

    # video input
    cap = cv2.VideoCapture(video_input)
    length = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    current_frame = first_frame
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)

    # video output
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    #out = cv2.VideoWriter(video_output, fourcc, fps / 5, (300, 200))

    cv2.namedWindow(CV_OUTPUT_WINDOW_NAME)
    cv2.createTrackbar( CV_FRAME_TRACKBAR_NAME, CV_OUTPUT_WINDOW_NAME, 0, 10000, onChange)

    onChange(current_frame)
    cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, current_frame)

    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            while(cap.isOpened()):
                ret, frame = cap.read()

                # only process every 5th frame for performance
                if current_frame % 5 == 0:
                    cv2.setTrackbarPos(CV_FRAME_TRACKBAR_NAME, CV_OUTPUT_WINDOW_NAME, int(cap.get(1)))

                    # convert from BGR to RGB
                    cv_input_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(cv_input_image)
                    
                    ratio = 0.5
                    size = image.size
                    resized_image = image.resize((int(size[0] * ratio), int(size[1] * ratio)), Image.ANTIALIAS)

                    # the array based representation of the image will be used later in order to prepare the
                    # result image with boxes and labels on it.
                    image_np = load_image_into_numpy_array(resized_image)
                    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                    image_np_expanded = np.expand_dims(image_np, axis=0)
                    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                    # Each box represents a part of the image where a particular object was detected.
                    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                    # Each score represent how level of confidence for each of the objects.
                    # Score is shown on the result image, together with the class label.
                    scores = detection_graph.get_tensor_by_name('detection_scores:0')
                    classes = detection_graph.get_tensor_by_name('detection_classes:0')
                    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
                    # Actual detection.
                    (boxes, scores, classes, num_detections) = sess.run(
                      [boxes, scores, classes, num_detections],
                      feed_dict={image_tensor: image_np_expanded})
                    # Visualization of the results of a detection.
                    vis_util.visualize_boxes_and_labels_on_image_array(
                        image_np,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        category_index,
                        use_normalized_coordinates=True,
                        line_thickness=8)

                    # convert from RGB to BGR
                    cv_output_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

                    #out.write(cv_output_image)
                    cv2.imshow(CV_OUTPUT_WINDOW_NAME, cv_output_image)
                    cv2.waitKey(1)

                current_frame +=1

    cap.release()
    #out.release()
    cv2.destroyAllWindows()
