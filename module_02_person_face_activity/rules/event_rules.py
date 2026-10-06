
"""
NEXORA Module 02
Person, Face & Activity Detection

Rule Engine

Responsibilities:
    Detection -> Temporal Validation -> Event

The detector/model does not decide whether an
activity becomes a NEXORA event.

This file contains only business/event rules.
"""


# --------------------------------------------------
# Event Rules
# --------------------------------------------------

EVENT_RULES = {

    "SITTING": {
        "severity": "LOW",
        "minimum_frames": 3
    },

    "STANDING": {
        "severity": "LOW",
        "minimum_frames": 3
    },

    "WALKING": {
        "severity": "LOW",
        "minimum_frames": 3
    },

    "RUNNING": {
        "severity": "MEDIUM",
        "minimum_frames": 3
    },

    "FALLING": {
        "severity": "HIGH",
        "minimum_frames": 3
    },

    "LYING": {
        "severity": "MEDIUM",
        "minimum_frames": 3
    },

    "RAISING_HAND": {
        "severity": "LOW",
        "minimum_frames": 3
    }
}


# --------------------------------------------------
# Valid statuses
# --------------------------------------------------

VALID_STATUSES = {
    "PENDING",
    "CONFIRMED",
    "DISMISSED",
    "UNCERTAIN",
    "RESOLVED"
}


# --------------------------------------------------
# Generate Event
# --------------------------------------------------

def generate_event(
    activity,
    camera_id,
    timestamp,
    confidence,
    track_id=None
):
    """
    Convert a validated activity into a NEXORA event.

    Parameters
    ----------
    activity : str
        Activity name.

    camera_id : str
        Camera identifier.

    timestamp : float
        Event timestamp.

    confidence : float
        Model/activity confidence.

    track_id : int or None
        Temporary person tracking ID.

    Returns
    -------
    dict or None
        Standard NEXORA event.
    """

    activity = activity.upper()

    # ----------------------------------------------
    # Check whether activity has an event rule
    # ----------------------------------------------

    if activity not in EVENT_RULES:

        return None


    rule = EVENT_RULES[activity]


    # ----------------------------------------------
    # Generate event ID
    # ----------------------------------------------

    import uuid

    event_id = (
        "EVT_"
        + uuid.uuid4().hex[:8].upper()
    )


    # ----------------------------------------------
    # Validate confidence
    # ----------------------------------------------

    confidence = float(confidence)

    confidence = max(
        0.0,
        min(1.0, confidence)
    )


    # ----------------------------------------------
    # Create standard event
    # ----------------------------------------------

    event = {

        "event_id": event_id,

        "module":
            "module_02_person_face_activity",

        "event_type":
            activity,

        "camera_id":
            camera_id,

        "track_id":
            track_id,

        "timestamp":
            timestamp,

        "confidence":
            round(confidence, 4),

        "severity":
            rule["severity"],

        "status":
            "PENDING",

        "rule": {

            "name":
                "persistent_activity",

            "threshold":
                0.5,

            "minimum_frames":
                rule["minimum_frames"]
        }
    }


    return event


# --------------------------------------------------
# Validate Event
# --------------------------------------------------

def validate_event(event):
    """
    Validate a generated NEXORA event.
    """

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


    # Check required fields

    for field in required_fields:

        if field not in event:

            return False


    # Check event type

    if event["event_type"] not in EVENT_RULES:

        return False


    # Check status

    if event["status"] not in VALID_STATUSES:

        return False


    # Check confidence

    if not (
        0.0
        <= event["confidence"]
        <= 1.0
    ):

        return False


    return True
