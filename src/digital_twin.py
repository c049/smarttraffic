# src/digital_twin.py

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg

def plot_digital_twin(detections, violations):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Display background map (optional)
    try:
        img = mpimg.imread("assets/streeet_map.png")  
        ax.imshow(img)
    except FileNotFoundError:
        ax.set_facecolor('lightgrey')
        ax.text(0.5, 0.5, 'No Map Found', ha='center', va='center', fontsize=18)

    # Draw detected objects (blue)
    for item in detections:
        center = item.get('center', [0, 0])
        label = item.get('label', 'object')
        x, y = center
        circ = patches.Circle((x, y), radius=10, edgecolor='blue', facecolor='none', linewidth=2)
        ax.add_patch(circ)
        ax.text(x + 10, y, label, color='blue', fontsize=8)

    # Draw violations (red)
    for item in violations:
        center = item.get('center', [0, 0])
        label = item.get('type', 'violation')  
        x, y = center
        circ = patches.Circle((x, y), radius=12, edgecolor='red', facecolor='none', linewidth=2)
        ax.add_patch(circ)
        ax.text(x + 10, y, label, color='red', fontsize=9, fontweight='bold')

    ax.set_title("Digital Twin Visualization")
    ax.axis('off')

    return fig  
