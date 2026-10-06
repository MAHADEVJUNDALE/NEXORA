
import json
import os
from pathlib import Path


MODULE_ID = "module_02_person_face_activity"


def load_json(path):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(data, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_pipeline_data(base_dir):
    base_dir = Path(base_dir)

    annotation_dir = (
        base_dir / "datasets" / "NEXORA_CCTV" / "annotations"
    )

    files = {
        "pipeline": annotation_dir / "pipeline_detection_results.json",
        "person": annotation_dir / "person_tracking_results.json",
        "face": annotation_dir / "face_detection_results.json",
        "pose": annotation_dir / "pose_detection_results.json",
        "activity": annotation_dir / "activity_results.json",
        "temporal": annotation_dir / "temporal_activity_results.json",
        "events": annotation_dir / "events.json",
        "incidents": annotation_dir / "incidents.json"
    }

    data = {}

    for name, path in files.items():
        if path.exists():
            data[name] = load_json(path)
        else:
            data[name] = []

    return data


def build_integrated_output(data):
    pipeline_results = data["pipeline"]

    activity_results = data["activity"]
    temporal_results = data["temporal"]
    events = data["events"]
    incidents = data["incidents"]

    integrated = {
        "module": MODULE_ID,
        "pipeline": {
            "detection": True,
            "tracking": len(data["person"]) > 0,
            "face_detection": len(data["face"]) > 0,
            "pose_detection": len(data["pose"]) > 0,
            "activity": len(activity_results) > 0,
            "temporal_validation": len(temporal_results) > 0,
            "event_generation": len(events) > 0,
            "incident_generation": len(incidents) > 0,
            "evidence": len(incidents) > 0
        },
        "statistics": {
            "frames": len(pipeline_results),
            "person_detections": len(data["person"]),
            "face_detections": len(data["face"]),
            "pose_detections": len(data["pose"]),
            "activity_detections": len(activity_results),
            "validated_sequences": len(temporal_results),
            "events": len(events),
            "incidents": len(incidents)
        },
        "events": events,
        "incidents": incidents
    }

    return integrated


def run_full_pipeline(
    base_dir="/content/NEXORA/module_02_person_face_activity"
):
    print("=" * 60)
    print("NEXORA MODULE 2 - FULL PIPELINE INTEGRATION")
    print("=" * 60)

    data = load_pipeline_data(base_dir)

    print()
    print("Loaded pipeline outputs:")
    print("Person detections :", len(data["person"]))
    print("Face detections   :", len(data["face"]))
    print("Pose detections   :", len(data["pose"]))
    print("Activity results  :", len(data["activity"]))
    print("Temporal results  :", len(data["temporal"]))
    print("Events            :", len(data["events"]))
    print("Incidents         :", len(data["incidents"]))

    integrated = build_integrated_output(data)

    output_dir = (
        Path(base_dir)
        / "datasets"
        / "NEXORA_CCTV"
        / "annotations"
    )

    output_path = output_dir / "full_pipeline_results.json"

    save_json(integrated, output_path)

    print()
    print("Integration completed successfully!")
    print("Output:")
    print(output_path)

    print()
    print("Pipeline status:")

    for key, value in integrated["pipeline"].items():
        status = "PASS" if value else "EMPTY"
        print(f"{key:25} : {status}")

    return integrated


if __name__ == "__main__":
    run_full_pipeline()
