import cv2
import numpy as np

OBJECT_TRACKER = {
    'crst' : cv2.legacy.TrackerCSRT_create,
    'mosse' : cv2.legacy.TrackerMOSSE_create,
    'kcf' : cv2.legacy.TrackerKCF_create,
}

trackers = cv2.legacy.MultiTracker_create()

video_path = './lostark_se_hanu_01.mp4' # './lostark_bm_hanu_01.mp4'

# 동영상 파일 열기
cap = cv2.VideoCapture(video_path)

for _ in range(100): #조우시까지 프레임 당기기
    cap.read()

frame_cnt = 0
count = 0
while True:
    frame_cnt += 1
    frame = cap.read()[1]

    if frame_cnt % 96 != 0:
        continue

    # frame = grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if frame is None:
        break

    # frame = cv2.resize(frame,(750,550))

    success, boxes = trackers.update(frame)

    if success == False:
        bound_boxes = trackers.getObjects()
        trackers_arr = np.array(trackers.getObjects())
        idx = np.where(trackers_arr.sum(axis=1) != 0)[0]
        trackers_arr = trackers_arr[idx]
        trackers = cv2.legacy.MultiTracker_create()
        for i in trackers_arr:
            tracker = cv2.legacy.TrackerCSRT_create()
            trackers.add(tracker, frame, tuple(i))

    for box in boxes:
        x,y,w,h = [int(c) for c in box]

        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0,0),2)

    cv2.imshow('tracking', frame)
    cv2.imwrite("./path_output_frame/%d.jpg" % count, frame)

    count+=1
    k = cv2.waitKey(30)

    if k == ord('s'):
        roi = cv2.selectROI('tracking', frame)
        traker = OBJECT_TRACKER['crst']()
        trackers.add(traker, frame, roi)

cap.release()
cv2.destroyAllWindows()
