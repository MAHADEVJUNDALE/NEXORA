
# NEXORA - Module 2: Person, Face & Activity Detection

## Module ID

module_02_person_face_activity

## 1. Overview

NEXORA Module 2 is responsible for Person Detection, Face Detection,
Human Pose Estimation and Activity Detection from CCTV or recorded video.

The module follows:

CCTV / Recorded Video
        |
        v
Video Ingestion
        |
        v
Frame Processing
        |
        v
Detection
        |
        v
Tracking
        |
        v
Pose / Activity Analysis
        |
        v
Temporal Validation
        |
        v
Rule Engine
        |
        v
Event
        |
        v
Incident
        |
        v
Evidence
        |
        v
Human Review


## 2. Objective

The main objectives are:

- Person detection
- Person counting
- Person tracking
- Face detection
- Human pose estimation
- Activity recognition
- Temporal activity validation
- Event generation
- Incident generation
- Evidence generation


## 3. Supported Detection

### Person Detection

The person detector identifies humans visible in the CCTV frame.

Output:

- Bounding box
- Confidence
- Temporary tracking ID when tracking is enabled


### Face Detection

The face detector identifies visible faces.

Output:

- Face bounding box
- Confidence
- Face visibility information when available

Important:

This module performs Face Detection, not Face Recognition.


### Pose Detection

The pose model estimates human body keypoints.

The current YOLO pose model provides 17 body keypoints.


## 4. Supported Activities

The current activity/event rules support:

- SITTING
- STANDING
- WALKING
- RUNNING
- FALLING
- LYING
- RAISING_HAND


## 5. Models

### Person Model

YOLO11n

Task:

Object Detection


### Face Model

YOLO11n-Face

Task:

Face Detection


### Pose Model

YOLO11n-Pose

Task:

Human Pose Estimation


### Tracking

Recommended tracker:

ByteTrack


## 6. Model Files

Models are stored in:

models/checkpoints/

Files:

- yolo11n.pt
- yolov11n-face.pt
- yolo11n-pose.pt


## 7. Datasets

The module requirements include:

### Person

- COCO
- CrowdHuman

### Face

- WIDER FACE

### Activity

- NTU RGB+D

### Custom Dataset

NEXORA CCTV Dataset

The custom dataset should contain realistic CCTV scenarios including:

- Different camera angles
- Different resolutions
- Different lighting
- Occlusion
- Different camera heights
- Different person distances
- Crowded scenes


## 8. Current Test Video

Current prototype testing uses:

datasets/NEXORA_CCTV/videos/coco_person_video.mp4

Properties:

- Frames: 100
- FPS: 10
- Resolution: 640 x 480

Important limitation:

This video is created from independent COCO images and is not a
continuous CCTV recording.

Therefore it is suitable for pipeline testing but not for valid
continuous tracking or temporal activity evaluation.


## 9. Project Structure

module_02_person_face_activity/
|
+-- README.md
|
+-- config/
|   +-- config.yaml
|
+-- datasets/
|
+-- models/
|   +-- checkpoints/
|   +-- exports/
|
+-- training/
|   +-- train.py
|   +-- validate.py
|   +-- augmentations.py
|
+-- inference/
|   +-- detector.py
|   +-- pipeline.py
|
+-- rules/
|   +-- event_rules.py
|
+-- tests/
|   +-- test_detection.py
|   +-- test_events.py
|   +-- test_edge_cases.py
|
+-- evaluation/
    +-- evaluate.py
    +-- results/


## 10. Configuration

Configuration file:

config/config.yaml

It contains:

- Model paths
- Input size
- Confidence thresholds
- IoU threshold
- Tracking configuration
- Temporal validation
- Event severity
- Evidence settings
- Output paths
- Camera configuration


## 11. Inference

The detector is available through:

from inference.detector import NexoraDetector

detector = NexoraDetector("config/config.yaml")

Available functions:

detector.detect_person(frame)

detector.detect_face(frame)

detector.detect_pose(frame)


## 12. Video Pipeline

Main pipeline function:

from inference.pipeline import process_video

results = process_video(
    source="datasets/NEXORA_CCTV/videos/coco_person_video.mp4",
    camera_id="CAM_01",
    config_path="config/config.yaml"
)


## 13. Pipeline Output

Pipeline output:

datasets/NEXORA_CCTV/annotations/pipeline_detection_results.json

The current pipeline performs:

Video
  |
  +-- Person Detection
  |
  +-- Face Detection
  |
  +-- Pose Detection
  |
  +-- Structured JSON


## 14. Standard Detection Fields

NEXORA detection records use:

- module
- camera_id
- frame_id
- timestamp
- track_id
- class_name
- confidence
- bbox


Example:

{
    "module": "module_02_person_face_activity",
    "camera_id": "CAM_01",
    "frame_id": 0,
    "timestamp": 0.0,
    "track_id": null,
    "class_name": "person",
    "confidence": 0.85,
    "bbox": {
        "x1": 100,
        "y1": 80,
        "x2": 250,
        "y2": 400
    }
}


## 15. Temporal Validation

The current configuration uses:

- Minimum frames: 3
- Cooldown frames: 10

Temporal validation reduces temporary detections and repeated frame-level
alerts.


## 16. Event Rules

Current event rules:

- SITTING - LOW
- STANDING - LOW
- WALKING - LOW
- RUNNING - MEDIUM
- FALLING - HIGH
- LYING - MEDIUM
- RAISING_HAND - LOW

Default event status:

PENDING


## 17. Evidence

Evidence frames are stored under:

datasets/NEXORA_CCTV/evidence/

Evidence allows a human reviewer to inspect generated incidents.


## 18. JSON Outputs

Current outputs include:

- person_tracking_results.json
- face_detection_results.json
- pose_detection_results.json
- activity_results.json
- temporal_activity_results.json
- events.json
- incidents.json
- pipeline_detection_results.json


## 19. Testing

Test files:

tests/test_detection.py
tests/test_events.py
tests/test_edge_cases.py

Current results:

Detection tests: 7/7 passed

Event tests: 8/8 passed

Edge-case tests: 9/9 passed

Total:

24/24 tests passed


## 20. Tested Scenarios

The tests include:

- Correct detections
- Incorrect detections
- Low confidence
- Multiple detections
- Small objects
- Occlusion
- Blur
- Persistent activity
- Temporary activity
- Cooldown
- Multiple tracks
- Low light
- Crowded scenes
- Camera movement
- Empty scenes
- Multiple-camera style inputs


## 21. Evaluation

Evaluation report:

evaluation/results/evaluation_report.json

Current prototype statistics:

- Person detections: 32
- Face detections: 170
- Pose detections: 128
- Activity detections: 124
- Validated sequences: 2
- Events: 2
- Incidents: 2

Average confidence:

- Person: 0.8269
- Face: 0.7593
- Pose: 0.7623


## 22. Evaluation Limitation

The current test video is not a continuous CCTV sequence.

Therefore the current prototype does not claim:

- Precision
- Recall
- mAP@50
- mAP@50:95
- HOTA
- IDF1
- Activity accuracy
- Activity F1

These metrics require proper ground-truth annotations and continuous
CCTV-style sequences.


## 23. False Positives

Possible false positives can occur because of:

- Poor lighting
- Motion blur
- Occlusion
- Crowded scenes
- Unusual camera angles
- Partial visibility
- Similar body poses


## 24. False Negatives

Possible false negatives can occur because of:

- Small persons
- Heavy occlusion
- Low-resolution video
- Poor illumination
- Extreme camera angles
- Fast movement


## 25. Architecture Separation

detector.py answers:

"What did the model detect?"

event_rules.py answers:

"Does this detection qualify as a NEXORA event?"

Model inference and event/business logic must remain separate.


## 26. Current Limitations

1. Current test video uses independent COCO images.
2. It is not a real continuous CCTV recording.
3. Activity recognition is currently a basic pose-based prototype.
4. Activity tracking is not yet fully associated with person track IDs.
5. Face detection does not perform face recognition.
6. Real CCTV validation is still required.
7. Production activity recognition requires stronger temporal modelling.
8. Quantitative metrics require proper ground truth.


## 27. Future Improvements

- Real continuous CCTV dataset
- Person-pose track association
- Improved activity recognition
- Fall detection
- Loitering detection
- Enter/exit detection
- Raising-hand detection
- Fighting-like motion detection
- Face-person association
- ByteTrack / BoT-SORT integration
- Evidence video clips
- Real CCTV evaluation
- Backend API integration
- Performance optimization


## 28. Hardware

The current prototype was tested using a GPU-enabled environment.

Required hardware depends on:

- Number of cameras
- Video resolution
- Required FPS
- Model size
- Tracking configuration
- Number of simultaneous streams


## 29. Dependencies

Main dependencies:

- Python
- OpenCV
- PyTorch
- Ultralytics
- PyYAML
- NumPy
- ByteTrack


## 30. Integration

The module should provide structured results to the NEXORA backend.

Frontend output may include:

- Bounding boxes
- Skeletons
- Tracking IDs
- Person count
- Activity labels
- Events
- Incidents
- Evidence references

The frontend should not depend directly on YOLO, PyTorch,
ByteTrack or RTMPose implementation details.


## 31. Module Status

Module:

module_02_person_face_activity

Status:

Prototype / Development
