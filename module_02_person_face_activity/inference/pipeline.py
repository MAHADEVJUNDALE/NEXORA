
import cv2
import json
import os
from inference.detector import NexoraDetector


def process_video(
    source: str,
    camera_id: str,
    config_path: str = "config/config.yaml"
):

    detector = NexoraDetector(config_path)

    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        raise ValueError(f"Unable to open video source: {source}")

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 30.0

    frame_id = 0

    results = []

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        timestamp = frame_id / fps

        # ------------------------------------------
        # PERSON DETECTION
        # ------------------------------------------

        person_detections = detector.detect_person(frame)

        # ------------------------------------------
        # FACE DETECTION
        # ------------------------------------------

        face_detections = detector.detect_face(frame)

        # ------------------------------------------
        # POSE DETECTION
        # ------------------------------------------

        pose_detections = detector.detect_pose(frame)

        # ------------------------------------------
        # STANDARD FRAME RESULT
        # ------------------------------------------

        frame_result = {
            "module": "module_02_person_face_activity",
            "camera_id": camera_id,
            "frame_id": frame_id,
            "timestamp": timestamp,
            "person_detections": person_detections,
            "face_detections": face_detections,
            "pose_detections": pose_detections
        }

        results.append(frame_result)

        frame_id += 1

    cap.release()

    return results


if __name__ == "__main__":

    video_path = (
        "datasets/NEXORA_CCTV/videos/"
        "coco_person_video.mp4"
    )

    output_path = (
        "datasets/NEXORA_CCTV/annotations/"
        "pipeline_detection_results.json"
    )

    results = process_video(
        source=video_path,
        camera_id="CAM_01",
        config_path="config/config.yaml"
    )

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    with open(output_path, "w") as file:
        json.dump(
            results,
            file,
            indent=4
        )

    print("Pipeline completed successfully.")
    print("Total frames processed:", len(results))
    print("Output saved to:")
    print(output_path)
