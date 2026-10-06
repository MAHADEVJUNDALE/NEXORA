
import json
import os


EVENTS_PATH = (
    "/content/NEXORA/module_02_person_face_activity/"
    "datasets/NEXORA_CCTV/annotations/events.json"
)

TEMPORAL_PATH = (
    "/content/NEXORA/module_02_person_face_activity/"
    "datasets/NEXORA_CCTV/annotations/temporal_activity_results.json"
)


VALID_EVENT_TYPES = {
    "SITTING",
    "STANDING",
    "WALKING",
    "RUNNING",
    "FALLING",
    "LYING",
    "RAISING_HAND"
}


VALID_SEVERITIES = {
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL"
}


VALID_STATUSES = {
    "PENDING",
    "CONFIRMED",
    "DISMISSED",
    "UNCERTAIN",
    "RESOLVED"
}


def load_events():

    with open(EVENTS_PATH, "r") as f:
        return json.load(f)


def load_temporal_results():

    with open(TEMPORAL_PATH, "r") as f:
        return json.load(f)


def test_events_file_exists():

    assert os.path.exists(EVENTS_PATH)


def test_events_not_empty():

    events = load_events()

    assert len(events) > 0


def test_required_event_fields():

    events = load_events()

    required_fields = [
        "event_id",
        "module",
        "event_type",
        "camera_id",
        "track_id",
        "timestamp",
        "confidence",
        "severity",
        "status"
    ]

    for event in events:

        for field in required_fields:

            assert field in event


def test_valid_event_type():

    events = load_events()

    for event in events:

        assert event["event_type"] in VALID_EVENT_TYPES


def test_valid_severity():

    events = load_events()

    for event in events:

        assert event["severity"] in VALID_SEVERITIES


def test_valid_status():

    events = load_events()

    for event in events:

        assert event["status"] in VALID_STATUSES


def test_event_confidence_range():

    events = load_events()

    for event in events:

        confidence = event["confidence"]

        assert 0.0 <= confidence <= 1.0


def test_temporal_validation():

    temporal_results = load_temporal_results()

    assert len(temporal_results) > 0

    for result in temporal_results:

        start_frame = result["start_frame"]
        end_frame = result["end_frame"]

        frame_count = end_frame - start_frame + 1

        assert frame_count >= 3
