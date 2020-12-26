import numpy as np
import os
import tensorflow as tf
import cv2
import pyautogui
#import time

from cv2 import CAP_PROP_FPS

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


image_message = None
gesture = ['None', 'up', 'down', 'left', 'right']
def play():
    # Đường dẫn frozen graph:
    PATH_TO_FROZEN_GRAPH = 'frozen_inference_graph/frozen_inference_graph.pb'

    # Đường dẫn label map
    PATH_TO_LABEL_MAP = 'images/object-detection.pbtxt'

    # Số lớp
    NUM_CLASSES = 4

    cap = cv2.VideoCapture(0)
    # test limit fps
    #cap.set(CAP_PROP_FPS, 5)
    #print("FPS: ", cap.get(CAP_PROP_FPS)) #=> 30


    # Đọc frozen graph
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.compat.v1.GraphDef()
        with tf.io.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    # Load label
    label_map = label_map_util.load_labelmap(PATH_TO_LABEL_MAP)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    # Nhận diện
    with detection_graph.as_default():
        with tf.compat.v1.Session(graph=detection_graph) as sess:
            while True:
                # Đọc frame từ camera
                #start = time.time()
                ret, image_np = cap.read()
                # Lật ngược ảnh
                image_np = np.fliplr(image_np)
                image_np = cv2.resize(image_np, (300, 300))
                # Mở rộng chiều => shape: [1, None, None, 3] (axis=0 => hàng)
                image_np_expanded = np.expand_dims(image_np, axis=0)
                #print(np.shape(image_np_expanded))
                # Extract image tensor
                image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                # Extract detection boxes
                boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                # Extract detection scores
                scores = detection_graph.get_tensor_by_name('detection_scores:0')
                # Extract detection classes
                classes = detection_graph.get_tensor_by_name('detection_classes:0')
                # Extract number of detections
                num_detections = detection_graph.get_tensor_by_name(
                    'num_detections:0')
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
                    line_thickness=3,
                    )
                # Display output
                image_message = image_np
                # Test resize
                cv2.imshow('Gesture Detection', cv2.resize(image_np, (600, 600)))
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
                '''MOVE'''

                objects = np.where(classes[0] == 1)[0]

                
                if len(objects) > 0 and scores[0][objects][0] > 0.8:
                    pyautogui.press('up')

                objects = np.where(classes[0] == 2)[0]

                
                if len(objects) > 0 and scores[0][objects][0] > 0.8:
                    pyautogui.press('down')

                objects = np.where(classes[0] == 3)[0]

                
                if len(objects) > 0 and scores[0][objects][0] > 0.8:
                    pyautogui.press('left')

                objects = np.where(classes[0] == 4)[0]

                
                if len(objects) > 0 and scores[0][objects][0] > 0.8:
                    pyautogui.press('right')
                #end = time.time()
                #print(end - start)
                

if __name__ == '__main__':
	play()              
