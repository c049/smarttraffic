# src/detection.py

def run_detection(source="sample.jpg"):
    print(f"📷 模拟检测已执行（处理图片：{source}）")

    # 返回伪造的“检测数据”
    detection_data = [
        {
            "type": "illegal_parking",
            "label": "car",
            "confidence": 0.92,
            "location": "X:100, Y:150"
        },
        {
            "type": "wrong_way",
            "label": "motorcycle",
            "confidence": 0.88,
            "location": "X:300, Y:240"
        }
    ]

    return detection_data
