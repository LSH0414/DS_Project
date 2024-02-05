from collections import defaultdict

import cv2
import numpy as np

from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Open the video file
video_path = "./lostark_bm_hanu_01.mp4"
cap = cv2.VideoCapture(video_path)

# Store the track history
track_history = defaultdict(lambda: [])

frame_cnt = 0
# Loop through the video frames
while cap.isOpened():
    frame_cnt += 1
    # Read a frame from the video
    success, frame = cap.read()

    if frame_cnt % 12 != 0:
        continue

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)

        # Get the boxes and track IDs
        boxes = results[0].boxes.xywh.cpu()
        # track_ids = results[0].boxes.id.int().cpu().tolist()
        # break

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Plot the tracks
        for box in boxes:
            x, y, w, h = box

            cv2.rectangle(frame,(int(x),int(y)),(int(w),int(h)),(255,0,0,255),2)

        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

print(results[0].boxes)
# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()