import pandas as pd
import cv2
import sys

sys.path.append("/home/jeans/internship/parking-customer-count")

from countpassenger.Config import conf
from countpassenger import Preprocess

import countpassenger
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os.path as osp
import os


df_cross = pd.read_csv(
    osp.join(conf.RESOURCES_RAW_DIR, "2024-04-28/mbk-tourist-raw-cross-object-20240428.csv")
)
df_cross = Preprocess.df_clean_customer(df_customer=df_cross)
df_cross = df_cross[df_cross["camera"] == "mbk-14-14"]

# Path to the video
video_path = "/mnt/c/OxygenAi/drop-pick/028/mbk-14-14_1714284001.mp4"

# Open the video file
cap = cv2.VideoCapture(video_path)

# Check if video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Read the first frame
ret, frame = cap.read()

# Release the video capture object
cap.release()

# Check if frame was read successfully
if not ret:
    print("Error: Could not read the first frame.")
    exit()

# Draw the bounding boxes on the frame
for index, row in df_cross.iterrows():
    x_min, x_max = row["xmin"], row["xmax"]
    y_min, y_max = row["ymin"], row["ymax"]
    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

# Display the frame with bounding boxes
cv2.imshow("Frame with Bounding Boxes", frame)
cv2.waitKey(0)  # Wait for a key press to close the window
cv2.destroyAllWindows()

# Optional: Save the frame with bounding boxes to a file
output_image_path = "output_frame.jpg"
cv2.imwrite(output_image_path, frame)
