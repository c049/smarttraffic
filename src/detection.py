# src/detection.py

import numpy as np

def run_detection(source="sample.jpg"):
    print(f"✅ 模拟检测已执行（处理图片: {source}）")

    # 创建一张白色图像并画两个框表示检测结果
    img = np.ones((400, 400, 3), dtype=np.uint8) * 255
    cv2.rectangle(img, (100, 150), (200, 250), (0, 255, 0), 2)  # car
    cv2.putText(img, "car", (100, 145), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.rectangle(img, (300, 240), (380, 320), (0, 0, 255), 2)  # motorcycle
    cv2.putText(img, "motorcycle", (300, 235), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # 保存为 output.jpg
    cv2.imwrite("output.jpg", img)

    # 返回模拟检测数据
    detection_data = [
        {
            "type": "illegal_parking",
            "label": "car",
            "confidence": 0.92,
            "location": "X:100, Y:150",
            "center": [150, 200]
        },
        {
            "type": "wrong_way",
            "label": "motorcycle",
            "confidence": 0.88,
            "location": "X:300, Y:240",
            "center": [340, 280]
        }
    ]

    return detection_data
