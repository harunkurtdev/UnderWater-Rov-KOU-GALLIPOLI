#encoding:utf-8
import cv2
import redis
import base64
import numpy as np

def base64_to_image(jpg_as_text):
    jpg_original = base64.b64decode(jpg_as_text)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    # jpg_as_np = np.fromstring(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    return img

rc = redis.StrictRedis(host="10.103.238.162", port="3799", db=0, decode_responses=True, password="123456")
ps = rc.pubsub()

# ps.subscribe('ch1')
ps.subscribe('ch3')

for item in ps.listen():
    # img = bytes(str(item['data']), encoding='utf8')
    if (isinstance(item['data'], str)):
        frame = base64_to_image(bytes(item['data'], encoding="utf8"))
        cv2.imshow("open", frame)
        cv2.waitKey(5)
    # print(type(item['data']))
# with open("F:\\tf-pose-estimation\\images\\4_2.png", "wb") as f:
#     f.write(data)
