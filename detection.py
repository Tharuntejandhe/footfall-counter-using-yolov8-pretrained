from ultralytics import YOLO

class PersonDetector:
    def __init__(self, device='cpu'):
        self.model = YOLO('yolov8m.pt')
        self.device = device
    
    def detect_people(self, frame):
        results = self.model(frame, device=self.device, classes=[0], verbose=False)
        boxes = []
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            conf = float(box.conf[0])
            if conf > 0.4:
                boxes.append([x1, y1, x2, y2])
        return boxes
