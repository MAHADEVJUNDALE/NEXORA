
from ultralytics import YOLO
import yaml
import os


class NexoraDetector:

    def __init__(self, config_path="config/config.yaml"):

        # Load configuration
        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)

        # Get module directory
        module_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        # Model paths from config
        person_model_path = os.path.join(
            module_dir,
            self.config["models"]["person"]["path"]
        )

        face_model_path = os.path.join(
            module_dir,
            self.config["models"]["face"]["path"]
        )

        pose_model_path = os.path.join(
            module_dir,
            self.config["models"]["pose"]["path"]
        )

        # Load models
        print("Loading Person Model...")
        self.person_model = YOLO(person_model_path)

        print("Loading Face Model...")
        self.face_model = YOLO(face_model_path)

        print("Loading Pose Model...")
        self.pose_model = YOLO(pose_model_path)

        print("All models loaded successfully.")


    # ==================================================
    # PERSON DETECTION
    # ==================================================

    def detect_person(self, frame):

        confidence = self.config[
            "inference"
        ][
            "confidence_threshold"
        ][
            "person"
        ]

        results = self.person_model.predict(
            source=frame,
            conf=confidence,
            classes=[0],
            verbose=False
        )

        detections = []

        for result in results:

            if result.boxes is None:
                continue

            for box in result.boxes:

                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = float(box.conf[0])

                detections.append({
                    "class_name": "person",
                    "confidence": conf,
                    "bbox": {
                        "x1": float(x1),
                        "y1": float(y1),
                        "x2": float(x2),
                        "y2": float(y2)
                    }
                })

        return detections


    # ==================================================
    # FACE DETECTION
    # ==================================================

    def detect_face(self, frame):

        confidence = self.config[
            "inference"
        ][
            "confidence_threshold"
        ][
            "face"
        ]

        results = self.face_model.predict(
            source=frame,
            conf=confidence,
            verbose=False
        )

        detections = []

        for result in results:

            if result.boxes is None:
                continue

            for box in result.boxes:

                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = float(box.conf[0])

                detections.append({
                    "class_name": "face",
                    "confidence": conf,
                    "bbox": {
                        "x1": float(x1),
                        "y1": float(y1),
                        "x2": float(x2),
                        "y2": float(y2)
                    }
                })

        return detections


    # ==================================================
    # POSE DETECTION
    # ==================================================

    def detect_pose(self, frame):

        confidence = self.config[
            "inference"
        ][
            "confidence_threshold"
        ][
            "pose"
        ]

        results = self.pose_model.predict(
            source=frame,
            conf=confidence,
            verbose=False
        )

        detections = []

        for result in results:

            if result.boxes is None:
                continue

            for i, box in enumerate(result.boxes):

                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = float(box.conf[0])

                keypoints = []

                if result.keypoints is not None:

                    points = result.keypoints.xy[i].tolist()

                    for point in points:

                        x, y = point

                        keypoints.append({
                            "x": float(x),
                            "y": float(y)
                        })

                detections.append({
                    "class_name": "person",
                    "confidence": conf,
                    "bbox": {
                        "x1": float(x1),
                        "y1": float(y1),
                        "x2": float(x2),
                        "y2": float(y2)
                    },
                    "keypoints": keypoints
                })

        return detections
