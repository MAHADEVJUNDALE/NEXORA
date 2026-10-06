
import os
import cv2
import json
from collections import defaultdict
from ultralytics import YOLO


# ============================================================
# CONFIG
# ============================================================

VIDEO = "/content/NEXORA/module_01_dangerous_object/datasets/cctv_video.mp4"

MODEL_PATH = "/content/NEXORA/module_01_dangerous_object/models/checkpoints/dangerous_object.pt"

OUTPUT_DIR = "/content/NEXORA/module_01_dangerous_object/outputs"

CONF = 0.15
FRAME_SKIP = 4
IMG_SIZE = 640
RESIZE_W = 640
RESIZE_H = 360
MIN_FRAMES = 3
COOLDOWN = 30

CAMERA_ID = "CAM_01"


# ============================================================
# DANGEROUS OBJECTS
# ============================================================

DANGEROUS = {
    "Firearm": "CRITICAL",
    "Explosive": "CRITICAL",
    "Melee_Weapon": "HIGH",
    "Blunt_Weapon": "HIGH"
}


# ============================================================
# CHECK FILES
# ============================================================

if not os.path.exists(VIDEO):
    raise FileNotFoundError(
        f"Video not found: {VIDEO}"
    )

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}"
    )

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading M01 model...")

model = YOLO(MODEL_PATH)

print("Model loaded.")
print("Classes:", model.names)


# ============================================================
# OPEN VIDEO
# ============================================================

cap = cv2.VideoCapture(VIDEO)

if not cap.isOpened():
    raise ValueError("Cannot open video")

FPS = cap.get(cv2.CAP_PROP_FPS)
TOTAL_FRAMES = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


print("\nVIDEO")
print("FPS:", FPS)
print("Frames:", TOTAL_FRAMES)
print("Resolution:", WIDTH, "x", HEIGHT)


# ============================================================
# OUTPUT VIDEO
# ============================================================

OUTPUT_VIDEO = os.path.join(
    OUTPUT_DIR,
    "dangerous_object_detection.mp4"
)

writer = cv2.VideoWriter(
    OUTPUT_VIDEO,
    cv2.VideoWriter_fourcc(*"mp4v"),
    FPS,
    (WIDTH, HEIGHT)
)


# ============================================================
# DATA
# ============================================================

detections = []
events = []
incidents = []

object_frame_count = defaultdict(int)
last_event_frame = defaultdict(lambda: -999999)

event_counter = 0
incident_counter = 0
frame_id = 0


# ============================================================
# PROCESS VIDEO
# ============================================================

print("\nProcessing video...")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_id += 1

    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        conf=CONF,
        verbose=False
    )

    result = results[0]

    annotated = frame.copy()

    if result.boxes is not None:

        boxes = result.boxes

        for i in range(len(boxes)):

            cls_id = int(boxes.cls[i])
            confidence = float(boxes.conf[i])

            class_name = model.names[cls_id]

            if boxes.id is not None:
                track_id = int(boxes.id[i])
            else:
                track_id = None

            x1, y1, x2, y2 = map(
                int,
                boxes.xyxy[i].tolist()
            )

            # ----------------------------------------
            # STANDARD DETECTION
            # ----------------------------------------

            detections.append({
                "module": "M01",
                "camera_id": CAMERA_ID,
                "frame_id": frame_id,
                "timestamp": round(frame_id / FPS, 3),
                "track_id": track_id,
                "class_name": class_name,
                "confidence": round(confidence, 4),
                "bbox": [x1, y1, x2, y2]
            })

            # ----------------------------------------
            # DANGEROUS OBJECT FILTER
            # ----------------------------------------

            if class_name not in DANGEROUS:
                continue

            severity = DANGEROUS[class_name]

            key = (
                track_id
                if track_id is not None
                else f"{class_name}_{x1}_{y1}"
            )

            object_frame_count[key] += 1

            # ----------------------------------------
            # DRAW BOX
            # ----------------------------------------

            cv2.rectangle(
                annotated,
                (x1, y1),
                (x2, y2),
                (0, 0, 255),
                2
            )

            cv2.putText(
                annotated,
                f"{class_name} {confidence:.2f}",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2
            )

            # ----------------------------------------
            # TEMPORAL VALIDATION
            # ----------------------------------------

            if object_frame_count[key] >= MIN_FRAMES:

                if (
                    frame_id - last_event_frame[key]
                    >= COOLDOWN
                ):

                    event_counter += 1

                    event_id = (
                        f"M01_EVT_{event_counter:04d}"
                    )

                    timestamp = round(
                        frame_id / FPS,
                        3
                    )

                    # EVENT
                    event = {
                        "event_id": event_id,
                        "module": "M01",
                        "event_type":
                            "DANGEROUS_OBJECT_DETECTED",
                        "camera_id": CAMERA_ID,
                        "track_id": track_id,
                        "timestamp": timestamp,
                        "confidence":
                            round(confidence, 4),
                        "severity": severity,
                        "status": "PENDING",
                        "rule":
                            "OBJECT_PERSISTED_FOR_3_FRAMES"
                    }

                    events.append(event)

                    # --------------------------------
                    # EVIDENCE
                    # --------------------------------

                    evidence_name = (
                        f"{event_id}_frame_{frame_id}.jpg"
                    )

                    evidence_path = os.path.join(
                        OUTPUT_DIR,
                        evidence_name
                    )

                    cv2.imwrite(
                        evidence_path,
                        annotated
                    )

                    # --------------------------------
                    # INCIDENT
                    # --------------------------------

                    incident_counter += 1

                    incident_id = (
                        f"M01_INC_{incident_counter:04d}"
                    )

                    incident = {
                        "incident_id": incident_id,
                        "module": "M01",
                        "title":
                            f"Dangerous {class_name} detected",
                        "event_type":
                            "DANGEROUS_OBJECT_DETECTED",
                        "camera_id": CAMERA_ID,
                        "timestamp": timestamp,
                        "severity": severity,
                        "confidence":
                            round(confidence, 4),
                        "status": "PENDING",

                        "evidence": {
                            "frame_id": frame_id,
                            "image": evidence_name,
                            "bbox": [
                                x1,
                                y1,
                                x2,
                                y2
                            ]
                        },

                        "review": {
                            "required": True,
                            "status": "PENDING"
                        }
                    }

                    incidents.append(incident)

                    last_event_frame[key] = frame_id

                    print(
                        f"EVENT: {class_name} | "
                        f"{severity} | "
                        f"Frame {frame_id}"
                    )

    # ----------------------------------------
    # FRAME NUMBER
    # ----------------------------------------

    cv2.putText(
        annotated,
        f"Frame: {frame_id}/{TOTAL_FRAMES}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    writer.write(annotated)


# ============================================================
# RELEASE
# ============================================================

cap.release()
writer.release()


# ============================================================
# SAVE JSON
# ============================================================

with open(
    os.path.join(
        OUTPUT_DIR,
        "detections.json"
    ),
    "w"
) as f:
    json.dump(detections, f, indent=2)


with open(
    os.path.join(
        OUTPUT_DIR,
        "events.json"
    ),
    "w"
) as f:
    json.dump(events, f, indent=2)


with open(
    os.path.join(
        OUTPUT_DIR,
        "incidents.json"
    ),
    "w"
) as f:
    json.dump(incidents, f, indent=2)


# ============================================================
# SUMMARY
# ============================================================

summary = {
    "module": "M01",
    "module_name": "Dangerous Object Detection",
    "video": VIDEO,
    "fps": FPS,
    "frames": TOTAL_FRAMES,
    "resolution": [WIDTH, HEIGHT],
    "total_detections": len(detections),
    "total_events": len(events),
    "total_incidents": len(incidents),
    "status": "COMPLETED"
}

with open(
    os.path.join(
        OUTPUT_DIR,
        "evaluation_summary.json"
    ),
    "w"
) as f:
    json.dump(summary, f, indent=2)


print("\n======================================")
print("M01 COMPLETED")
print("======================================")
print("Detections :", len(detections))
print("Events     :", len(events))
print("Incidents  :", len(incidents))
print("Output     :", OUTPUT_DIR)
print("======================================")
