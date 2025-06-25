# src/dashboard.py

import streamlit as st
from src.detection import run_detection
from src.violation_logic import check_illegal_parking, check_wrong_way
from src.digital_twin import plot_digital_twin
from src.map_view import draw_map_view
import os

def show_dashboard():
    st.set_page_config(page_title="Smart Traffic Dashboard", layout="wide")

    st.title("🚦 AI + Digital Twin Traffic Violation Detection")
    st.markdown("利用计算机视觉 + 数字孪生技术，实现 **违停** 和 **逆行** 实时监测与可视化。")

    # ⬆ 上传图像
    uploaded_file = st.file_uploader("📤 上传街景图片（或使用默认 sample.jpg）", type=["jpg", "png"])

    if uploaded_file is not None:
        img_path = "sample.jpg"
        with open(img_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success("✅ 图片上传成功")
    else:
        st.warning("⚠️ 未上传图片，将使用默认图像 sample.jpg")

    # 🚀 开始检测
    if st.button("🚗 开始检测与分析"):
        with st.spinner("正在进行目标检测与违章分析..."):
            detections = run_detection(source="sample.jpg")

            parking_violations = check_illegal_parking(detections)
            wrong_way_violations = check_wrong_way(detections)
            all_violations = parking_violations + wrong_way_violations

            # 🔍 可视化图像
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📷 YOLO 检测结果图")
                st.image("output.jpg", caption="检测结果图像", use_column_width=True)

            with col2:
                st.subheader("🗺 数字孪生地图展示")
                fig = plot_digital_twin(detections, all_violations)
                st.pyplot(fig)


            # 📄 数据结构化展示
            st.subheader("📋 检测对象结构化数据")
            st.json(detections)

            st.subheader("🚫 违章车辆信息")
            st.json(all_violations)

            # 🧭 抽象地图绘图
            st.subheader("🧭 抽象 MapView 显示")
            st.pyplot(lambda: draw_map_view(detections, all_violations))




