# src/map_view.py

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_map_view(detections, violations):
    """
    detections: list of dicts with 'center', 'label'
    violations: list of dicts with 'object_id', 'type'
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # 1️⃣ 背景路段
    ax.set_facecolor("lightgray")
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 600)

    # 2️⃣ 道路线条（横向两车道）
    ax.add_patch(patches.Rectangle((0, 250), 800, 100, color="white", zorder=0))
    ax.plot([0, 800], [300, 300], linestyle="--", color="gray")

    # 3️⃣ 禁停区域（左上、右下）
    ax.add_patch(patches.Rectangle((100, 350), 100, 50, color="red", alpha=0.4))
    ax.add_patch(patches.Rectangle((600, 200), 100, 50, color="red", alpha=0.4))

    # 4️⃣ 方向箭头（右向）
    ax.arrow(50, 280, 100, 0, head_width=10, head_length=20, fc='black', ec='black')
    ax.text(60, 290, "→", fontsize=15, weight='bold')

    # 5️⃣ 映射车辆（红色违章 / 蓝色正常）
    violated_ids = {v["object_id"]: v["type"] for v in violations}

    for i, obj in enumerate(detections):
        cx, cy = obj["center"]
        label = obj["label"]
        color = "red" if i in violated_ids else "blue"

        # 绘制车辆圆点
        ax.plot(cx, cy, marker='o', markersize=10, color=color)
        ax.text(cx + 5, cy + 5, label, fontsize=8, color=color)

        # 如果违章，标记类型
        if i in violated_ids:
            vtype = violated_ids[i]
            ax.text(cx + 5, cy - 15, f"🚫 {vtype}", color='red', fontsize=9)

    ax.set_title("🛣 Map View - Traffic Layout & Violations")
    ax.axis('off')
    plt.tight_layout()
    plt.show()


# ✅ 测试用例（可删除）
if __name__ == "__main__":
    test_detections = [
        {"label": "car", "center": [120, 370], "bbox": [100, 360, 140, 390]},
        {"label": "car", "center": [640, 220], "bbox": [620, 210, 660, 240]},
        {"label": "bus", "center": [300, 280], "bbox": [280, 250, 340, 310]},
    ]

    test_violations = [
        {"type": "Illegal Parking", "object_id": 0},
        {"type": "Wrong-Way Driving", "object_id": 1}
    ]

    draw_map_view(test_detections, test_violations)
