# src/digital_twin.py

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg

def plot_digital_twin(detections, violations):
    # 创建画布和坐标系
    fig, ax = plt.subplots(figsize=(8, 6))

    # 显示背景地图图像（assets 中）
    try:
        img = mpimg.imread("assets/streeet_map.png")  # 注意拼写是否一致
        ax.imshow(img)
    except FileNotFoundError:
        ax.set_facecolor('lightgrey')
        ax.text(0.5, 0.5, 'No Map Found', ha='center', va='center', fontsize=18)

    # 添加正常检测对象（蓝框）
    for item in detections:
        box = item.get('box', {})
        label = item.get('label', 'object')
        x, y, w, h = box.get('x', 0), box.get('y', 0), box.get('w', 40), box.get('h', 40)
        rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor='blue', facecolor='none')
        ax.add_patch(rect)
        ax.text(x, y - 10, label, color='blue', fontsize=8)

    # 添加违章对象（红框+文字）
    for item in violations:
        box = item.get('box', {})
        label = item.get('violation', 'violation')
        x, y, w, h = box.get('x', 0), box.get('y', 0), box.get('w', 40), box.get('h', 40)
        rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor='red', facecolor='none')
        ax.add_patch(rect)
        ax.text(x, y - 10, label, color='red', fontsize=8, fontweight='bold')

    ax.set_title("Digital Twin Visualization")
    ax.axis('off')

    return fig  # ✅ 注意：必须返回 fig 对象

