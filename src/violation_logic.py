# src/violation_logic.py

import math

# 假设的禁停区域列表（你可以根据地图标注具体坐标）
# 每个区域为 [x1, y1, x2, y2]
NO_PARK_ZONES = [
    [100, 100, 300, 300],  # 示例：地图上某一块区域为禁停区
    [500, 400, 700, 550]
]

# 模拟上一帧车辆中心位置（实际部署中应由视频帧维护）
last_positions = {}  # 结构: {object_id: (x, y)}

def is_in_zone(point, zone):
    x, y = point
    x1, y1, x2, y2 = zone
    return x1 <= x <= x2 and y1 <= y <= y2

def check_illegal_parking(detections, static_threshold=3):
    """
    假设某对象连续 static_threshold 帧中心点几乎不动（静止），且处于禁停区域内，则为违停
    """
    violations = []

    for i, obj in enumerate(detections):
        label = obj["label"]
        center = tuple(obj["center"])

        if label != "car" and label != "bus" and label != "truck":
            continue

        # 简化：我们用 obj 的 index 作为 id
        obj_id = i

        if obj_id in last_positions:
            old_center = last_positions[obj_id]
            distance = math.dist(center, old_center)

            # 若移动距离非常小，判断为静止状态
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
    基于车辆中心点的前后变化方向判断是否逆行（简化实现）
    expected_direction 可设为 "right" 或 "left"
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


# ✅ 示例用法
if __name__ == "__main__":
    # 模拟输入（真实调用时来自 detection.py 的结果）
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
