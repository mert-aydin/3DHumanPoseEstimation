import mediapipe as mp
import cv2
import sys
from tqdm import tqdm


class PoseDetection():
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
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

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

    def find(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

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

def show(data, detector, name):
    cap = cv2.VideoCapture(data)
    size = int(cap.get(3)),int(cap.get(4))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Video Size: {size}")
    print(f"Processing Video: {frame_count} frames")
    result = cv2.VideoWriter(
        f'{name}',
        cv2.VideoWriter_fourcc(*'mp4v'),
        20,
        size,
    )
    for _ in tqdm(range(frame_count), desc="Processing Video"):
        has_frame, frame = cap.read()
        if not has_frame:
            break

        frame = detector.find(frame)
        cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        result.write(frame)
    cap.release()
    result.release()

show(input_filename, PoseDetection(), output_filename)
