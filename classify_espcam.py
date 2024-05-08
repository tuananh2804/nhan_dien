import sys
import os

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import copy
import cv2
import urllib.request
import base64

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow.compat.v1 as tf

username = "admin"
password = "admin123"

def predict(image_data):

    predictions = sess.run(softmax_tensor, \
             {'DecodeJpeg/contents:0': image_data})

    # Sort to show labels of first prediction in order of confidence
    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

    max_score = 0.0
    res = ''
    for node_id in top_k:
        human_string = label_lines[node_id]
        score = predictions[0][node_id]
        if score > max_score:
            max_score = score
            res = human_string
    return res, max_score

# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line
                   in tf.gfile.GFile("logs/trained_labels.txt")]

# Unpersists graph from file
with tf.gfile.FastGFile("logs/trained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

with tf.Session() as sess: 
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    c = 0

    #cap = cv2.VideoCapture(0)
    url = 'http://192.168.119.220/cam.mjpeg'
    res, score = '', 0.0
    i = 0
    mem = ''
    consecutive = 0
    sequence = ''
    loop_count = 0
    # image_count = image_end - image_start
    
    capture = False
    message = ''
    img = None
    img_cropped = None
    in_loop = True
    
    auth_header = 'Basic ' + base64.b64encode(f'{username}:{password}'.encode()).decode()
    request = urllib.request.Request(url)
    request.add_header('Authorization', auth_header)
    while in_loop:
        imgResp = urllib.request.urlopen(request)
        bytes = b''
        while True:
            bytes += imgResp.read(1024)
            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')
           
            if a != -1 and b != -1:
                jpg = bytes[a:b + 2]
                bytes = bytes[b + 2:]
                img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                img = cv2.flip(img, 1)
                x1, y1, x2, y2 = 100, 100, 300, 300
                img_cropped = img[y1:y2, x1:x2]

                c += 1
                flag = cv2.waitKey(1)
                    
            # imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
            # img = cv2.imdecode(imgNp,-1)
            # # img = cap.read()
            # img = cv2.flip(img, 1)
            # # 
            
            # x1, y1, x2, y2 = 100, 100, 300, 300
            # img_cropped = img[y1:y2, x1:x2]

                
                try:
                    image_data = cv2.imencode('.jpg', img_cropped)[1].tostring()
                except:
                    continue
                    
                #     #waits to see if `esc` is pressed
                
                if i == 10:
                    res_tmp, score = predict(image_data)
                    res = res_tmp
                    i = 0
                    if mem == res:
                        consecutive += 1
                    else:
                        consecutive = 0
                    if consecutive == 2 and res not in ['nothing']:
                        if res == 'space':
                            sequence += ' '
                        elif res == 'del':
                            sequence = sequence[:-1]
                        else:
                            sequence += res
                        consecutive = 0
                i += 1
                cv2.putText(img, '%s' % (res.upper()), (100,400), cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255), 4)
                cv2.putText(img, '(score = %.5f)' % (float(score)), (100,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
                mem = res
                cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2)
                cv2.imshow("img", img)
                img_sequence = np.zeros((200,1200,3), np.uint8)
                cv2.putText(img_sequence, '%s' % (sequence.upper()), (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                cv2.imshow('sequence', img_sequence)
        
                if flag == 27:
                    in_loop = False
                    break
        if not in_loop:
         break

# Following line should... <-- This should work fine now
cv2.destroyAllWindows() 
cv2.VideoCapture(0).release()