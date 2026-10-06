
import json
import os


ANNOTATION_PATH = (
    "/content/NEXORA/module_02_person_face_activity/"
    "datasets/NEXORA_CCTV/annotations/person_tracking_results.json"
)


def load_detections():

    with open(ANNOTATION_PATH, "r") as f:
        return json.load(f)


def test_detection_file_exists():

    assert os.path.exists(ANNOTATION_PATH)


def test_detection_not_empty():

    detections = load_detections()

    assert len(detections) > 0


def test_required_fields():

    detections = load_detections()

    required_fields = [
        "module",
        "camera_id",
        "frame_id",
        "timestamp",
        "track_id",
        "class_name",
        "confidence",
        "bbox"
    ]

    for detection in detections:

        for field in required_fields:

            assert field in detection


def test_person_class():

    detections = load_detections()

    for detection in detections:

        assert detection["class_name"] == "person"


def test_confidence_range():

    detections = load_detections()

    for detection in detections:

        confidence = detection["confidence"]

        assert 0.0 <= confidence <= 1.0


def test_bbox_format():

    detections = load_detections()

    for detection in detections:

        bbox = detection["bbox"]

        assert len(bbox) == 4

        x1 = bbox["x1"]
        y1 = bbox["y1"]
        x2 = bbox["x2"]
        y2 = bbox["y2"]

        assert x1 < x2
        assert y1 < y2


def test_track_id_present():

    detections = load_detections()

    track_ids = [
        detection["track_id"]
        for detection in detections
        if detection["track_id"] is not None
    ]

    assert len(track_ids) > 0
