
import json
import os
import statistics


BASE_PATH = (
    "/content/NEXORA/module_02_person_face_activity"
)

PERSON_PATH = os.path.join(
    BASE_PATH,
    "datasets/NEXORA_CCTV/annotations/person_tracking_results.json"
)

FACE_PATH = os.path.join(
    BASE_PATH,
    "datasets/NEXORA_CCTV/annotations/face_detection_results.json"
)

POSE_PATH = os.path.join(
    BASE_PATH,
    "datasets/NEXORA_CCTV/annotations/pose_detection_results.json"
)

ACTIVITY_PATH = os.path.join(
    BASE_PATH,
    "datasets/NEXORA_CCTV/annotations/activity_results.json"
)

TEMPORAL_PATH = os.path.join(
    BASE_PATH,
    "datasets/NEXORA_CCTV/annotations/temporal_activity_results.json"
)

EVENT_PATH = os.path.join(
    BASE_PATH,
    "datasets/NEXORA_CCTV/annotations/events.json"
)

INCIDENT_PATH = os.path.join(
    BASE_PATH,
    "datasets/NEXORA_CCTV/annotations/incidents.json"
)

OUTPUT_PATH = os.path.join(
    BASE_PATH,
    "evaluation/results/evaluation_report.json"
)


def load_json(path):

    if not os.path.exists(path):
        return []

    with open(path, "r") as f:
        return json.load(f)


def average_confidence(data):

    if not data:
        return 0.0

    values = [
        float(item["confidence"])
        for item in data
        if "confidence" in item
    ]

    if not values:
        return 0.0

    return round(statistics.mean(values), 4)


# -----------------------------------------
# Load results
# -----------------------------------------

persons = load_json(PERSON_PATH)
faces = load_json(FACE_PATH)
poses = load_json(POSE_PATH)
activities = load_json(ACTIVITY_PATH)
temporal = load_json(TEMPORAL_PATH)
events = load_json(EVENT_PATH)
incidents = load_json(INCIDENT_PATH)


# -----------------------------------------
# Activity distribution
# -----------------------------------------

activity_distribution = {}

for item in activities:

    activity = item.get(
        "activity",
        item.get("class_name", "UNKNOWN")
    )

    activity_distribution[activity] = (
        activity_distribution.get(activity, 0) + 1
    )


# -----------------------------------------
# Event distribution
# -----------------------------------------

event_distribution = {}

for event in events:

    event_type = event["event_type"]

    event_distribution[event_type] = (
        event_distribution.get(event_type, 0) + 1
    )


# -----------------------------------------
# Tracking information
# -----------------------------------------

track_ids = set()

for person in persons:

    track_id = person.get("track_id")

    if track_id is not None:
        track_ids.add(track_id)


# -----------------------------------------
# Evaluation report
# -----------------------------------------

report = {

    "module":
        "module_02_person_face_activity",

    "evaluation_note":
        "Metrics are calculated from the current "
        "prototype outputs. The COCO-derived video "
        "contains non-continuous frames, therefore "
        "ground-truth accuracy metrics such as mAP, "
        "precision, recall, HOTA, IDF1 and activity "
        "accuracy are not claimed.",

    "detection": {

        "person_detections":
            len(persons),

        "face_detections":
            len(faces),

        "pose_detections":
            len(poses),

        "average_person_confidence":
            average_confidence(persons),

        "average_face_confidence":
            average_confidence(faces),

        "average_pose_confidence":
            average_confidence(poses)
    },

    "tracking": {

        "unique_track_ids":
            len(track_ids),

        "tracking_records":
            len(persons)
    },

    "activity": {

        "activity_detections":
            len(activities),

        "activity_distribution":
            activity_distribution,

        "average_activity_confidence":
            average_confidence(activities)
    },

    "temporal_validation": {

        "validated_activity_sequences":
            len(temporal)
    },

    "events": {

        "total_events":
            len(events),

        "event_distribution":
            event_distribution
    },

    "incidents": {

        "total_incidents":
            len(incidents)
    }
}


# -----------------------------------------
# Save report
# -----------------------------------------

with open(OUTPUT_PATH, "w") as f:

    json.dump(
        report,
        f,
        indent=2
    )


# -----------------------------------------
# Console output
# -----------------------------------------

print("==========================================")
print("NEXORA MODULE 02 EVALUATION")
print("==========================================")

print()

print("Person detections :", len(persons))
print("Face detections   :", len(faces))
print("Pose detections   :", len(poses))

print()

print(
    "Avg person confidence :",
    average_confidence(persons)
)

print(
    "Avg face confidence   :",
    average_confidence(faces)
)

print(
    "Avg pose confidence   :",
    average_confidence(poses)
)

print()

print(
    "Unique track IDs      :",
    len(track_ids)
)

print(
    "Activity detections   :",
    len(activities)
)

print(
    "Validated sequences   :",
    len(temporal)
)

print(
    "Total events          :",
    len(events)
)

print(
    "Total incidents       :",
    len(incidents)
)

print()

print("Activity distribution:")
print(activity_distribution)

print()

print("Event distribution:")
print(event_distribution)

print()

print("Evaluation report saved at:")
print(OUTPUT_PATH)
