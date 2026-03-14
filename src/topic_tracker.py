"""
Weak Topic Tracker — tracks how many times a student revisits a topic.
Higher count = weaker topic = needs more attention.
"""

import json
import os

TRACKER_FILE = "data/topic_tracker.json"


def update_tracker(tracker: dict, topic: str) -> dict:
    """Increment visit count for a topic."""
    topic = topic.strip().lower()
    tracker[topic] = tracker.get(topic, 0) + 1
    _save_tracker(tracker)
    return tracker


def get_weak_topics(tracker: dict, min_visits: int = 2) -> dict:
    """
    Return topics visited more than min_visits times, sorted by frequency.
    These are the student's weak areas.
    """
    weak = {k: v for k, v in tracker.items() if v >= min_visits}
    return dict(sorted(weak.items(), key=lambda x: x[1], reverse=True))


def reset_tracker():
    """Clear the tracker file."""
    if os.path.exists(TRACKER_FILE):
        os.remove(TRACKER_FILE)


def load_tracker() -> dict:
    """Load tracker from file if it exists."""
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r") as f:
            return json.load(f)
    return {}


def _save_tracker(tracker: dict):
    """Persist tracker to JSON file."""
    os.makedirs("data", exist_ok=True)
    with open(TRACKER_FILE, "w") as f:
        json.dump(tracker, f, indent=2)
