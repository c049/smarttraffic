import streamlit as st
from src.detection import run_detection
from src.violation_logic import check_illegal_parking, check_wrong_way
from src.digital_twin import plot_digital_twin
from src.map_view import draw_map_view

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image


def show_dashboard():
    st.set_page_config(page_title="Smart Traffic Dashboard", layout="wide")

    st.title("🚦AI + Digital Twin Traffic Violation Detection")
    st.markdown("Combining computer vision and digital twin technologies for real-time monitoring and visualization of illegal parking 🚗 and wrong-way driving 🏍️.")

    # 📤 Upload an image.
    uploaded_file = st.file_uploader("📤 Upload an image for detection (or use default sample.jpg)", type=["jpg", "png"])

    if uploaded_file is not None:
        img_path = "sample.jpg"
        with open(img_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success("✅ Image uploaded successfully")
    else:
        st.warning("⚠️ No image uploaded. Using default Sample.jpeg")
        img_path = "assets/Sample.jpeg"

    # 🚀 Start detection
    if st.button("🚗 Start Detection & Analysis"):
        with st.spinner("Running traffic violation detection and image analysis..."):
            detections = run_detection(source=img_path)

            # ✨ Violation logic
            parking_violations = check_illegal_parking(detections)
            wrong_way_violations = check_wrong_way(detections)
            all_violations = parking_violations + wrong_way_violations

            # 📊 Visualization
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📷 Detection Result Image")
                image = Image.open(img_path)
                fig, ax = plt.subplots()
                ax.imshow(image)

                for item in detections:
                    x1, y1, x2, y2 = item["bbox"]
                    label = item["label"]
                    color = 'red' if item["type"] == "wrong_way" else 'blue'

                    rect = patches.Rectangle((x1, y1), x2 - x1, y2 - y1,
                                             linewidth=2, edgecolor=color, facecolor='none')
                    ax.add_patch(rect)
                    ax.text(x1, y1 - 10, label, color=color, fontsize=10)

                ax.axis("off")
                st.pyplot(fig)

            with col2:
                st.subheader("🚨 Violation List")
                for v in all_violations:
                    st.markdown(
                     f"- 🚨 **{v.get('type', 'Unknown Type')}** by `{v.get('label', 'Unknown Label')}` at `{v.get('location', v.get('center', 'Unknown Location'))}`"
                     f" (Confidence: {v.get('confidence', 'N/A')})"
                    )


            st.subheader("🧠 Digital Twin Visualization")
            plot_digital_twin(detections, all_violations)

            st.subheader("🗺️ Map Visualization")
            draw_map_view(detections, all_violations)

    st.markdown("---")
    st.header("📘 Project Background & Description")

    with st.expander("📖 Introduction"):
        st.markdown("""
        Illegal parking and wrong-way driving are persistent challenges in urban areas, leading to congestion, safety risks, and inefficient road usage. Traditional enforcement relies heavily on manual monitoring, which is time-consuming and lacks scalability.

        This project introduces an AI-powered, real-time traffic violation detection system integrated with Digital Twin technology. By analyzing CCTV or street camera footage using deep learning algorithms (e.g., YOLOv8, OpenCV tracking), the system detects vehicles parked in restricted zones or moving against designated directions.

        Detection results are synchronized with a virtual Digital Twin—a dynamic 3D model that mirrors actual road conditions in real-time. This enables authorities to visually monitor violations, simulate traffic disruptions, and evaluate countermeasures.

        The system supports deployment on devices like Raspberry Pi and NVIDIA Jetson, making it scalable across urban streets, schools, and intersections.

        Future development includes V2X communication, automated alerts, and educational feedback.
        """)

    with st.expander("🧪 Method"):
        st.markdown("""
        **• Data Collection & Annotation**  
        Traffic footage from public datasets and simulated scenarios was used. Key frames were annotated with bounding boxes and motion directions to train detection models.

        **• Model Architecture**  
        We utilize YOLOv8 for object detection, customized to recognize vehicle types and orientations. Optical flow and lane detection algorithms are integrated to identify wrong-way driving behavior.

        **• Violation Detection Logic**  
        - *Illegal Parking*: Vehicles stationary in restricted zones beyond a set duration are flagged.  
        - *Wrong-Way Driving*: Vehicles moving against traffic flow or lane markings are detected and highlighted.

        **• Digital Twin Integration**  
        Violations are mirrored in a 3D Digital Twin model of the city for intuitive visualization of locations and traffic disruptions.

        **• Real-Time Monitoring Dashboard**  
        A Streamlit dashboard presents camera feeds, alerts, and violation summaries.

        **• Scalability & Deployment**  
        Designed for edge devices (e.g., Raspberry Pi, Jetson), supporting urban-wide scalability.
        """)

    with st.expander("📷 Results"):
        st.markdown("""
        This demo showcases real-time detection via a YOLOv8-based urban surveillance system. It accurately identifies buses, pedestrians, and signs, allowing enforcement of illegal parking and wrong-way driving. All results are visualized in a dashboard for automated violation analysis and enforcement.
        """)
        st.image("assets/resultdemo.png", caption="Detection and 3D Digital Twin Visualization")

    with st.expander("📌 Conclusion"):
        st.markdown("""
        This project highlights the practical potential of combining AI-powered traffic surveillance with Digital Twin technology to address urban traffic violations.

        It enables real-time detection and virtual visualization of illegal behaviors. The platform is scalable and can expand to monitor red-light running or speeding with traffic analytics, V2X communication, and smart city infrastructure.

        This provides a sustainable, intelligent traffic enforcement solution.
        """)

    with st.expander("📚 References"):
        st.markdown("""
        1. Z. Rahman, M. A. Ami, and M. A. Ullah, “A Real-Time Wrong-Way Vehicle Detection Based on YOLO and Centroid Tracking,” IEEE Xplore, Jun. 01, 2020. [Link](https://ieeexplore.ieee.org/document/9230463)

        2. M. Jafari et al., “A Review on Digital Twin Technology in Smart Grid, Transportation System and Smart City,” IEEE Access, 2023. [DOI](https://doi.org/10.1109/access.2023.3241588)

        3. C. Hu et al., “Digital Twin-Assisted Real-Time Traffic Data Prediction,” IEEE Trans., 2022. [DOI](https://doi.org/10.1109/TII.2021.3083596)

        4. X. Peng et al., “Illegal Parking Detection Algorithm,” IEEE Trans. on ITS, 2022. [DOI](https://doi.org/10.1109/TITS.2022.3180225)

        5. M. S. Irfan et al., “Toward Transportation Digital Twin Systems,” IEEE IoT Journal, 2024. [DOI](https://doi.org/10.1109/jiot.2024.3395186)

        6. Y. Wu, K. Zhang, “Digital Twin Networks: A Survey,” IEEE IoT Journal, 2021. [DOI](https://doi.org/10.1109/jiot.2021.3079510)
        """)
