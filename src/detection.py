# src/detection.py
from ultralytics import YOLO
import cv2
import os
MODEL_PATH = 'yolov8n.pt'
SOURCE_PATH = 'sample.jpg'
SAVE_RESULT = True

def run_detection(model_path=MODEL_PATH, source=SOURCE_PATH):
    model = YOLO(model_path)

    if source.endswith('.jpg') or source.endswith('.png'):
        img = cv2.imread(source)
        if img is None:
            print("❌ 图像加载失败，请检查路径")
            return
    else:
        print("❌ 暂时只支持图片输入")
        return

    results = model(source)
    print(f"✅ 检测完成，共检测到 {len(results[0].boxes)} 个对象")

    annotated = results[0].plot()

    if SAVE_RESULT:
        cv2.imwrite("output.jpg", annotated)
        print("📸 检测结果已保存为 output.jpg")

    detection_data = []
    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        cls_id = int(box.cls[0].item())
        conf = float(box.conf[0].item())
        label = model.names[cls_id]
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        detection_data.append({
            "label": label,
            "confidence": round(conf, 2),
            "bbox": [round(x1), round(y1), round(x2), round(y2)],
            "center": [round(center_x), round(center_y)]
        })

    return detection_data

if __name__ == '__main__':
    data = run_detection()
    print("\n🎯 检测结构化数据预览：")
    for obj in data:
        print(obj)

