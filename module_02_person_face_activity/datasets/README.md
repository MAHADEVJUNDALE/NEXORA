
# NEXORA Module 2 - Dataset Documentation

## Module ID

module_02_person_face_activity


## 1. Purpose

This directory contains datasets used for Person Detection, Face Detection,
Human Pose Estimation and Activity Recognition for NEXORA Module 2.

The datasets are used for:

- Model development
- Model testing
- Detection validation
- Pose estimation
- Activity recognition
- CCTV scenario evaluation


## 2. Dataset Structure

datasets/
|
+-- COCO/
|
+-- CrowdHuman/
|
+-- WIDER_FACE/
|
+-- NTU_RGBD/
|
+-- NEXORA_CCTV/
|   |
|   +-- videos/
|   +-- annotations/
|   +-- evidence/
|
+-- README.md


## 3. COCO

### Dataset Name

COCO - Common Objects in Context

### Purpose

COCO is used for general object and person detection.

For this module, the person class is used for testing the Person Detection
pipeline.

### Relevant Class

- person

### Annotation Type

Bounding-box object annotations.

### Current Local Dataset

The COCO validation dataset is stored at:

datasets/COCO/

Current verification:

- Images: 5000
- Annotated images: 5000
- Object annotations: 36781
- Classes: 80
- Person class ID: 1

### Usage

COCO is currently used for:

- Person detection testing
- Detection pipeline testing
- Prototype video generation


## 4. CrowdHuman

### Dataset Name

CrowdHuman

### Purpose

CrowdHuman is intended for crowded-person detection scenarios.

It is useful for testing person detection when multiple people are present
or when persons are partially occluded.

### Main Use

- Crowded person detection
- Occlusion handling
- Person detection robustness

### Current Status

Dataset is part of the planned Module 2 dataset structure.

A complete training/evaluation result should only be reported after the
dataset is actually downloaded, prepared and evaluated.


## 5. WIDER FACE

### Dataset Name

WIDER FACE

### Purpose

WIDER FACE is intended for face detection.

It provides challenging face detection examples with variations such as:

- Different face sizes
- Different poses
- Occlusion
- Crowded scenes
- Different imaging conditions

### Main Use

- Face detector development
- Face detection validation
- Small-face testing

### Current Status

WIDER FACE is included in the planned dataset structure.

No training or evaluation metric is claimed until the dataset is actually
prepared and evaluated.


## 6. NTU RGB+D

### Dataset Name

NTU RGB+D

### Purpose

NTU RGB+D is intended for human activity recognition and action
understanding.

### Main Use

- Activity recognition research
- Temporal activity modelling
- Human action analysis

### Activity Requirement

Activity recognition should use sequences rather than only individual
images.

### Current Status

NTU RGB+D is part of the planned Module 2 dataset structure.

No activity accuracy is claimed from this dataset until it is actually
prepared and evaluated.


## 7. NEXORA CCTV Dataset

### Dataset Name

NEXORA CCTV Dataset

### Purpose

The custom NEXORA CCTV dataset is required for realistic CCTV validation.

It should represent the actual operating conditions expected by NEXORA.

### Recommended Data Conditions

The dataset should include:

- Actual CCTV camera angle
- Different camera heights
- Different resolutions
- Different lighting conditions
- Day and night scenarios
- Different person distances
- Partial visibility
- Occlusion
- Crowded scenes
- Empty scenes
- Motion blur
- Different camera positions


## 8. Custom Dataset Classes

The custom dataset may contain annotations required for:

### Person

- Person bounding box
- Person visibility
- Tracking identity where available

### Face

- Face bounding box
- Face visibility
- Occlusion information where available

### Pose

- Human body keypoints

### Activity

Predefined activities include:

- Standing
- Sitting
- Walking
- Running
- Falling
- Lying
- Raising hand
- Fighting-like motion
- Entering
- Exiting
- Loitering


## 9. Annotation Requirements

Person detection annotations should contain:

- Image/frame ID
- Bounding box
- Class
- Visibility information where available

Face detection annotations should contain:

- Face bounding box
- Image/frame ID
- Visibility/occlusion information where available

Pose annotations should contain:

- Person bounding box
- Body keypoints

Activity annotations should contain:

- Person/track ID where available
- Activity label
- Start frame
- End frame
- Activity duration where available


## 10. Dataset Splitting

Dataset splitting should avoid leakage between similar video frames.

For CCTV data, the preferred split is by:

- Camera
- Session
- Video sequence

and not simply by adjacent frames.

This prevents nearly identical frames from appearing in both training and
testing data.


## 11. Preprocessing

Possible preprocessing includes:

- Image resizing
- Frame extraction
- Bounding-box validation
- Annotation validation
- Removing corrupted files
- Resolution normalization
- Timestamp/frame synchronization

The preprocessing procedure should be recorded when a dataset is prepared.


## 12. Data Augmentation

Potential augmentation techniques include:

- Horizontal flipping
- Scaling
- Cropping
- Brightness changes
- Contrast changes
- Blur
- Noise
- Rotation where appropriate

Augmentation should represent realistic CCTV conditions and should not
create unrealistic training examples.


## 13. Hard Negatives

Hard-negative examples should be included where possible.

Examples:

- Objects incorrectly detected as persons
- Posters containing people
- Reflections
- Shadows
- Partial persons
- Very small persons
- Heavy occlusion
- Motion blur
- Low-light scenes


## 14. Dataset Quality Checks

Before training or evaluation, check:

- Corrupted images
- Missing annotations
- Invalid bounding boxes
- Incorrect class labels
- Duplicate samples
- Extremely small objects
- Missing frames
- Incorrect timestamps
- Invalid video files


## 15. Current Prototype Video

A prototype video was generated from COCO images:

datasets/NEXORA_CCTV/videos/coco_person_video.mp4

Properties:

- Frames: 100
- FPS: 10
- Resolution: 640 x 480

Important limitation:

The frames originate from separate COCO images and are not a continuous
CCTV sequence.

Therefore this video is useful for:

- Detection pipeline testing
- Model integration testing
- JSON output testing

It should not be treated as a valid continuous tracking or activity
recognition benchmark.


## 16. Dataset Limitations

Current limitations include:

1. The custom NEXORA CCTV dataset is still required for realistic testing.
2. COCO is a general-purpose dataset and is not a dedicated CCTV dataset.
3. The prototype COCO video does not provide true temporal continuity.
4. Activity evaluation requires continuous labelled sequences.
5. Tracking evaluation requires reliable identity annotations.
6. Detection metrics require proper ground-truth annotations.


## 17. Dataset Source Information

For every dataset used in the final project, maintain the following
information:

- Dataset name
- Official source
- URL
- License
- Download date
- Purpose
- Classes
- Annotation format
- Train/validation/test split
- Preprocessing
- Augmentation
- Known limitations

The final project should record the actual source URL and license information
when each external dataset is formally added.


## 18. Data Privacy

CCTV data may contain identifiable individuals.

Any real NEXORA CCTV dataset must be collected and handled according to the
applicable privacy, consent, security and organizational requirements.

Real CCTV data should not be shared publicly unless appropriate permission
and legal requirements are satisfied.


## 19. Dataset Status

Current status:

Prototype / Development

Available and verified:

- COCO validation dataset
- COCO-based prototype video

Planned/required:

- CrowdHuman
- WIDER FACE
- NTU RGB+D
- Custom NEXORA CCTV Dataset


## 20. Final Dataset Goal

The final NEXORA Module 2 dataset should support evaluation of:

- Person Detection
- Face Detection
- Pose Estimation
- Person Tracking
- Activity Recognition
- Temporal Validation
- Event Detection

The dataset should contain realistic continuous CCTV sequences and
appropriate ground-truth annotations before final performance metrics are
reported.
