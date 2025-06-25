# src/detection.py

def run_detection(source="sample.jpg"):
    print(f"✅ 模拟检测已执行（处理图片: {source}）")

    # 返回模拟检测数据（不需要用 cv2，也不保存图片）
    detection_data = [
        {
            "type": "illegal_parking",
            "label": "car",
            "confidence": 0.92,
            "location": "X:100, Y:150",
            "center": [150, 200],
            "bbox": [100, 150, 200, 250]
        },
        {
            "type": "wrong_way",
            "label": "motorcycle",
            "confidence": 0.88,
            "location": "X:300, Y:240",
            "center": [340, 280],
            "bbox": [300, 240, 380, 320]
        }
    ]

    return detection_data
