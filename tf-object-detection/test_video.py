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

VIDEO_RESIZE_RATIO = 0.5
VIDEO_DETECTION_DIVIDER = 10


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


if __name__ == '__main__':
    args = parse_args()

    video_input = args.video_input
    video_output = args.video_output
    first_frame = int(args.first_frame)

    # video input
    cap = cv2.VideoCapture(video_input)
    if cap.isOpened:
        print('video capture opened')
    else:
        print('failed to open')
        

    cap.set(cv2.CAP_PROP_POS_FRAMES, first_frame)

    video_original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_original_total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_original_fps = float(cap.get(cv2.CAP_PROP_FPS))
    
    print('width: %s, height: %s, frames: %s, fps: %s' %(video_original_width, video_original_height, video_original_total_frames, video_original_fps))
    video_resized_width = int(video_original_width * VIDEO_RESIZE_RATIO)
    video_resized_height = int(video_original_height * VIDEO_RESIZE_RATIO)

    video_detection_fps = float(video_original_fps / VIDEO_DETECTION_DIVIDER)
    video_detection_wait_time = int(1000 / video_detection_fps)

    # video output
    #fourcc = cv2.FOURCC('M', 'P', 'E', 'G')
    fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
    out = cv2.VideoWriter(video_output, fourcc, video_detection_fps, (video_resized_width, video_resized_height), True)


    #cv2.namedWindow(CV_OUTPUT_WINDOW_NAME)


    detection_graph = tf.Graph()

    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            while (cap.isOpened()):
                next_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                cap.grab()

                if next_frame % VIDEO_DETECTION_DIVIDER == 0:
                    ret, frame = cap.retrieve()
                    print('processing frame ' + str(next_frame) + ' of ' + str(video_original_total_frames))
                    # convert from BGR to RGB
                    cv_input_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(cv_input_image)
                    size = image.size
                    resized_image = image.resize((video_resized_width, video_resized_height), Image.ANTIALIAS)

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

                    #cv2.imshow(CV_OUTPUT_WINDOW_NAME, cv_output_image)
                    out.write(cv_output_image)

                    if cv2.waitKey(video_detection_wait_time) & 0xFF == ord('q'):
                        break
                if next_frame == video_original_total_frames:
                    break

    cap.release()
    out.release()
    #cv2.destroyAllWindows()
