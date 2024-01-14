import mediapipe as mp
import cv2
import sys
from tqdm import tqdm


# Class for pose detection using MediaPipe library
class PoseDetection:
    def __init__(
            self,
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            enable_segmentation=False,
            smooth_segmentation=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
    ):
        # Initialize parameters for pose detection
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        # Initialize MediaPipe drawing utilities and pose model
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode,
            model_complexity,
            smooth_landmarks,
            enable_segmentation,
            smooth_segmentation,
            min_detection_confidence,
            min_tracking_confidence,
        )

    # Method to find pose landmarks in an image
    def find(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img_rgb)

        # Draw pose landmarks on the image if detected
        if self.results.pose_landmarks:
            if draw:
                self.mp_drawing.draw_landmarks(
                    img,
                    self.results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                )

        return img


# Specify the input/output video file paths
filename = 'demo' if len(sys.argv) < 2 else sys.argv[1]
input_filename = filename + '.mp4'
output_filename = filename + '_output_mediapipe.mp4'

# Set the frame rate for the output video (should match input video frame rate)
output_frames_per_second = 25


# Function to process video frames using the pose detector
def show(data, detector, name):
    # Open video capture from file
    cap = cv2.VideoCapture(data)
    size = int(cap.get(3)), int(cap.get(4))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Video Size: {size}")
    print(f"Processing Video: {frame_count} frames")

    # Create a VideoWriter object for the output video
    result = cv2.VideoWriter(
        f'{name}',
        cv2.VideoWriter_fourcc(*'mp4v'),
        output_frames_per_second,
        size,
    )

    # Process each frame in the video
    for _ in tqdm(range(frame_count), desc="Processing Video"):
        has_frame, frame = cap.read()
        if not has_frame:
            break

        # Find pose landmarks in the frame using the detector
        frame = detector.find(frame)
        cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Display the processed frame and write it to the output video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        result.write(frame)

    # Release video capture and writer objects
    cap.release()
    result.release()


# Process the input video using the PoseDetection class and save the output
show(input_filename, PoseDetection(), output_filename)
