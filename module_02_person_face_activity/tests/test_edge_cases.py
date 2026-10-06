
import os
import json


PERSON_PATH = (
    "/content/NEXORA/module_02_person_face_activity/"
    "datasets/NEXORA_CCTV/annotations/person_tracking_results.json"
)

ACTIVITY_PATH = (
    "/content/NEXORA/module_02_person_face_activity/"
    "datasets/NEXORA_CCTV/annotations/activity_results.json"
)

EVENTS_PATH = (
    "/content/NEXORA/module_02_person_face_activity/"
    "datasets/NEXORA_CCTV/annotations/events.json"
)


def load_json(path):

    with open(path, "r") as f:
        return json.load(f)


def test_empty_scene():

    empty_detections = []

    assert len(empty_detections) == 0


def test_multiple_persons():

    detections = load_json(PERSON_PATH)

    track_ids = {
        d["track_id"]
        for d in detections
        if d["track_id"] is not None
    }

    assert len(track_ids) >= 1


def test_valid_frame_ids():

    detections = load_json(PERSON_PATH)

    for detection in detections:

        assert isinstance(
            detection["frame_id"],
            int
        )

        assert detection["frame_id"] >= 0


def test_valid_timestamps():

    detections = load_json(PERSON_PATH)

    for detection in detections:

        assert detection["timestamp"] >= 0


def test_bbox_inside_valid_coordinates():

    detections = load_json(PERSON_PATH)

    for detection in detections:

        bbox = detection["bbox"]

        assert bbox["x1"] >= 0
        assert bbox["y1"] >= 0
        assert bbox["x2"] >= 0
        assert bbox["y2"] >= 0


def test_activity_results_exist():

    assert os.path.exists(ACTIVITY_PATH)

    activities = load_json(ACTIVITY_PATH)

    assert len(activities) > 0


def test_activity_confidence_valid():

    activities = load_json(ACTIVITY_PATH)

    for activity in activities:

        confidence = activity["confidence"]

        assert 0.0 <= confidence <= 1.0


def test_events_have_valid_camera():

    events = load_json(EVENTS_PATH)

    for event in events:

        assert event["camera_id"] is not None
        assert event["camera_id"] != ""


def test_events_have_valid_module():

    events = load_json(EVENTS_PATH)

    for event in events:

        assert (
            event["module"]
            == "module_02_person_face_activity"
        )
