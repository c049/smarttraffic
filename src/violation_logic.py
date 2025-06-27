# src/violation_logic.py

import math

# Presumed no-parking zones (you can mark specific coordinates based on map)
# Each zone is defined as [x1, y1, x2, y2]
NO_PARK_ZONES = [
    [100, 100, 300, 300],  # Example: a zone on the map where parking is forbidden
    [500, 400, 700, 550]
]

# Simulated previous frame center positions (should be tracked per video frame in actual deployment)
last_positions = {}  # Structure: {object_id: (x, y)}

def is_in_zone(point, zone):
    x, y = point
    x1, y1, x2, y2 = zone
    return x1 <= x <= x2 and y1 <= y <= y2

def check_illegal_parking(detections, static_threshold=3):
    """
    If an object’s center remains almost stationary for static_threshold frames
    and is within a no-parking zone, it is considered illegally parked.
    """
    violations = []

    for i, obj in enumerate(detections):
        label = obj["label"]
        center = tuple(obj["center"])

        if label != "car" and label != "bus" and label != "truck":
            continue

        # Simplified: use index as object ID
        obj_id = i

        if obj_id in last_positions:
            old_center = last_positions[obj_id]
            distance = math.dist(center, old_center)

            # If movement distance is very small, consider it stationary
            if distance < 5:
                for zone in NO_PARK_ZONES:
                    if is_in_zone(center, zone):
                        violations.append({
                            "type": "Illegal Parking",
                            "object_id": obj_id,
                            "center": center,
                            "zone": zone
                        })
                        break
        last_positions[obj_id] = center

    return violations


def check_wrong_way(detections, expected_direction="right"):
    """
    Determine wrong-way driving based on the direction change of object center
    (simplified implementation). expected_direction can be "right" or "left".
    """
    violations = []

    for i, obj in enumerate(detections):
        label = obj["label"]
        center = tuple(obj["center"])

        if label not in ["car", "bus", "truck"]:
            continue

        obj_id = i
        if obj_id in last_positions:
            old_x = last_positions[obj_id][0]
            new_x = center[0]
            delta_x = new_x - old_x

            if expected_direction == "right" and delta_x < -10:
                violations.append({
                    "type": "Wrong-Way Driving",
                    "object_id": obj_id,
                    "from_x": old_x,
                    "to_x": new_x
                })
            elif expected_direction == "left" and delta_x > 10:
                violations.append({
                    "type": "Wrong-Way Driving",
                    "object_id": obj_id,
                    "from_x": old_x,
                    "to_x": new_x
                })

        last_positions[obj_id] = center

    return violations


# ✅ Example usage
if __name__ == "__main__":
    # Simulated input (in actual use, comes from detection.py)
    test_detections = [
        {"label": "car", "center": [120, 150], "bbox": [100, 100, 140, 200]},
        {"label": "car", "center": [510, 420], "bbox": [490, 400, 530, 440]},
        {"label": "person", "center": [200, 250], "bbox": [180, 220, 220, 280]}
    ]

    park_vio = check_illegal_parking(test_detections)
    wrong_vio = check_wrong_way(test_detections)

    print("\n🚫 Parking Violations:")
    for v in park_vio:
        print(v)

    print("\n🔁 Wrong-Way Driving:")
    for v in wrong_vio:
        print(v)
