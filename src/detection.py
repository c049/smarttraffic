# src/detection.py

# def run_detection 是模拟的，不调用YOLO模型

def run_detection(source="sample.jpg"):
    print(f"✅ 模拟检测已执行 (处理图片: {source})")

    # 返回伪造的“检测结果”
    detection_data = [
        {
            "type": "illegal_parking",
            "label": "car",
            "confidence": 0.92,
            "center": [100, 150],  # ✅ 添加 center 坐标
        },
        {
            "type": "wrong_way",
            "label": "motorcycle",
            "confidence": 0.88,
            "center": [300, 240],  # ✅ 添加 center 坐标
        }
    ]

    return detection_data
