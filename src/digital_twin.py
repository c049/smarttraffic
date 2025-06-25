# src/digital_twin.py

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg

def plot_digital_twin(detections, violations):
    fig, ax = plt.subplots(figsize=(8, 6))

    # 背景地图（可选）
    try:
        img = mpimg.imread("assets/streeet_map.png")  # 确保拼写没错
        ax.imshow(img)
    except FileNotFoundError:
        ax.set_facecolor('lightgrey')
        ax.text(0.5, 0.5, 'No Map Found', ha='center', va='center', fontsize=18)

    # 绘制正常目标（蓝圈）
    for item in detections:
        center = item.get('center', [0, 0])
        label = item.get('label', 'object')
        x, y = center
        circ = patches.Circle((x, y), radius=10, edgecolor='blue', facecolor='none', linewidth=2)
        ax.add_patch(circ)
        ax.text(x + 10, y, label, color='blue', fontsize=8)

    # 绘制违规目标（红圈）
    for item in violations:
        center = item.get('center', [0, 0])
        label = item.get('type', 'violation')  # 原来是 'violation'，改成 'type'
        x, y = center
        circ = patches.Circle((x, y), radius=12, edgecolor='red', facecolor='none', linewidth=2)
        ax.add_patch(circ)
        ax.text(x + 10, y, label, color='red', fontsize=9, fontweight='bold')

    ax.set_title("Digital Twin Visualization")
    ax.axis('off')

    return fig  # ✅ 保留返回 fig
