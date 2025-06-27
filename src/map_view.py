# src/map_view.py

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st

def draw_map_view(detections, violations):
    """
    detections: list of dicts with 'center', 'label'
    violations: list of dicts with 'center', 'type'
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Background road section
    ax.set_facecolor("lightgray")
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 600)

    # Lane divider (double yellow line)
    ax.add_patch(patches.Rectangle((0, 250), 800, 100, color="white", zorder=0))
    ax.plot([0, 800], [300, 300], linestyle="--", color="gray")

    # No-parking areas
    ax.add_patch(patches.Rectangle((100, 350), 100, 50, color="red", alpha=0.4))
    ax.add_patch(patches.Rectangle((600, 200), 100, 50, color="red", alpha=0.4))

    # Direction arrow
    ax.arrow(50, 280, 100, 0, head_width=10, head_length=20, fc='black', ec='black')
    ax.text(60, 290, "→", fontsize=15, weight='bold')

    # Extract violation coordinates
    violation_centers = [tuple(v.get("center", [0, 0])) for v in violations]

    # Draw objects (car, motorcycle)
    for obj in detections:
        cx, cy = obj["center"]
        label = obj["label"]
        is_violation = (cx, cy) in violation_centers

        color = "red" if is_violation else "blue"
        ax.plot(cx, cy, marker='o', markersize=10, color=color)
        ax.text(cx + 5, cy + 5, label, fontsize=8, color=color)

        if is_violation:
            ax.text(cx + 5, cy - 15, f"🚫", color='red', fontsize=10)

    ax.set_title("🛣 Map View - Traffic Layout & Violations")
    ax.axis('off')
    plt.tight_layout()
    st.pyplot(fig)
