import streamlit as st
from src.detection import run_detection
from src.violation_logic import check_illegal_parking, check_wrong_way
from src.digital_twin import plot_digital_twin
from src.map_view import draw_map_view
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def show_dashboard():
    st.set_page_config(page_title="Smart Traffic Dashboard", layout="wide")

    st.title("🚦AI + Digital Twin Traffic Violation Detection")
    st.markdown("利用计算机视觉 + 数字孪生技术，实现违章停车 🚗 和 逆行 🏍️ 实时监测与可视化。")

    # 📤 上传图像
    uploaded_file = st.file_uploader("📤 上传待检测图片（或使用默认 sample.jpg）", type=["jpg", "png"])

    if uploaded_file is not None:
        img_path = "sample.jpg"
        with open(img_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success("✅ 图片上传成功")
    else:
        st.warning("⚠️ 未上传图片，将使用默认 sample.jpg")

    # 🚀 开始检测
    if st.button("🚗 开始检测与分析"):
        with st.spinner("正在进行交通违规检测与图像分析..."):
            detections = run_detection(source="sample.jpg")

            # ✨ 违规逻辑分析
            parking_violations = check_illegal_parking(detections)
            wrong_way_violations = check_wrong_way(detections)
            all_violations = parking_violations + wrong_way_violations

            # 📊 可视化展示
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📷 检测结果图像")
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.set_xlim(0, 400)
                ax.set_ylim(0, 400)
                ax.set_facecolor("lightgray")

                for item in detections:
                    x1, y1, x2, y2 = item["bbox"]
                    label = item["label"]
                    color = 'red' if item["type"] == "wrong_way" else 'blue'

                    rect = patches.Rectangle((x1, y1), x2 - x1, y2 - y1,
                                             linewidth=2, edgecolor=color, facecolor='none')
                    ax.add_patch(rect)
                    ax.text(x1, y1 - 10, label, color=color, fontsize=10)

                ax.invert_yaxis()  # 如果图像坐标系与预期反向
                st.pyplot(fig)

            with col2:
                st.subheader("违规行为列表")
                for v in all_violations:
                    st.markdown(
                        f"- 🚨 **{v['type']}** by `{v['label']}` at `{v.get('location', v.get('center'))}`"
                        f" (置信度 {v.get('confidence', 'N/A')})"
                    )

            st.subheader("🧠 数字孪生视图")
            plot_digital_twin(detections, all_violations)

            st.subheader("🗺️ 地图可视化")
            draw_map_view(detections, all_violations)
