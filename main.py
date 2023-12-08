import sys

# Import OpenCV library for computer vision tasks
import cv2 as cv
from tqdm import tqdm

# Specify the input video file path
filename = 'demo' if len(sys.argv) < 2 else sys.argv[1]
input_filename = filename + '.mp4'

# Set the resolution of the input video file
file_size = (640, 360)

# Define the output video file path
output_filename = filename + '_output.mp4'

# Set the frame rate for the output video
output_frames_per_second = 20.0

# Define key body parts and their indices for pose estimation
BODY_PARTS = {"Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
              "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
              "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
              "LEye": 15, "REar": 16, "LEar": 17, "Background": 18}

# Define pairs of body parts to connect for visualizing the human skeleton
POSE_PAIRS = [["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
              ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
              ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
              ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
              ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"]]

# Load the pre-trained neural network model for pose estimation
net = cv.dnn.readNetFromTensorflow("graph_opt.pb")

# Open the video file for reading
cap = cv.VideoCapture(input_filename)

# Create a VideoWriter object to write the processed video
result = cv.VideoWriter(output_filename, cv.VideoWriter_fourcc(*'mp4v'),
                        output_frames_per_second, file_size)

# Process the video frame by frame with a progress bar
frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

for _ in tqdm(range(frame_count), desc="Processing Video"):
    hasFrame, frame = cap.read()
    if not hasFrame:
        break

    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]

    # Prepare the frame for neural network input
    net.setInput(cv.dnn.blobFromImage(frame, 1.0, (368, 368), (127.5, 127.5, 127.5), swapRB=True, crop=False))
    out = net.forward()

    # Extract the first 19 elements (corresponding to the body parts) from the network output
    out = out[:, :19, :, :]

    points = []
    for i in range(len(BODY_PARTS)):
        heatMap = out[0, i, :, :]

        # Find the global maximum in the heatMap to get the most confident point of the body part
        _, conf, _, point = cv.minMaxLoc(heatMap)
        x = (frameWidth * point[0]) / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]

        # Add the detected point to the points list if its confidence is high enough
        points.append((int(x), int(y)) if conf > 0.2 else None)

    # Draw lines and ellipses to connect and represent the detected body parts
    for pair in POSE_PAIRS:
        partFrom = pair[0]
        partTo = pair[1]

        idFrom = BODY_PARTS[partFrom]
        idTo = BODY_PARTS[partTo]

        if points[idFrom] and points[idTo]:
            cv.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
            cv.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (255, 0, 0), cv.FILLED)
            cv.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (255, 0, 0), cv.FILLED)

    # Write process time of each frame
    t, _ = net.getPerfProfile()
    freq = cv.getTickFrequency() / 1000
    cv.putText(frame, '%.2fms' % (t / freq), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    # Write the processed frame to the output video
    result.write(frame)

# Release the video capture and writer resources
cap.release()
result.release()
