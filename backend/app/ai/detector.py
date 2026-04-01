import cv2
import numpy as np
from ultralytics import YOLO
import logging
from typing import Generator
import base64
import json

logger = logging.getLogger(__name__)

class PeopleDetector:
    def __init__(self):
        # YOLOv8n — fastest model, great for CPU
        self.model = YOLO("yolov8n.pt")
        self.model.overrides["verbose"] = False
        # Only detect people (class 0)
        self.person_class = 0
        self.confidence_threshold = 0.45
        logger.info("YOLOv8n model loaded successfully")

    def detect(self, frame: np.ndarray) -> list:
        """Run detection on a single frame"""
        results = self.model(
            frame,
            classes=[self.person_class],
            conf=self.confidence_threshold,
            verbose=False
        )
        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                detections.append({
                    "bbox": [x1, y1, x2, y2],
                    "confidence": round(confidence, 3),
                    "class": "person",
                    "center": [
                        int((x1 + x2) / 2),
                        int((y1 + y2) / 2)
                    ]
                })
        return detections

    def draw_boxes(self, frame: np.ndarray, detections: list) -> np.ndarray:
        """Draw bounding boxes on frame"""
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            conf = det["confidence"]
            color = (0, 200, 255)  # cyan

            # Bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            # Corner brackets
            bracket = 20
            thickness = 3
            # Top-left
            cv2.line(frame, (x1, y1), (x1 + bracket, y1), color, thickness)
            cv2.line(frame, (x1, y1), (x1, y1 + bracket), color, thickness)
            # Top-right
            cv2.line(frame, (x2, y1), (x2 - bracket, y1), color, thickness)
            cv2.line(frame, (x2, y1), (x2, y1 + bracket), color, thickness)
            # Bottom-left
            cv2.line(frame, (x1, y2), (x1 + bracket, y2), color, thickness)
            cv2.line(frame, (x1, y2), (x1, y2 - bracket), color, thickness)
            # Bottom-right
            cv2.line(frame, (x2, y2), (x2 - bracket, y2), color, thickness)
            cv2.line(frame, (x2, y2), (x2, y2 - bracket), color, thickness)

            # Label
            label = f"Person {int(conf * 100)}%"
            cv2.rectangle(frame, (x1, y1 - 22), (x1 + 110, y1), color, -1)
            cv2.putText(frame, label, (x1 + 4, y1 - 6),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        # People count
        count_text = f"People: {len(detections)}"
        cv2.rectangle(frame, (8, 8), (160, 36), (0, 0, 0), -1)
        cv2.putText(frame, count_text, (14, 28),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)

        return frame

    def frame_to_base64(self, frame: np.ndarray) -> str:
        """Convert frame to base64 for WebSocket streaming"""
        _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        return base64.b64encode(buffer).decode("utf-8")


class WebcamStream:
    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        self.cap = None
        self.detector = PeopleDetector()
        self.is_running = False

    def start(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 15)
        self.is_running = True
        logger.info(f"Webcam {self.camera_index} started")

    def stop(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
        logger.info("Webcam stopped")

    def get_frame_with_detections(self):
        """Get one frame with detections drawn"""
        if not self.cap or not self.cap.isOpened():
            return None, []
        ret, frame = self.cap.read()
        if not ret:
            return None, []
        detections = self.detector.detect(frame)
        annotated = self.detector.draw_boxes(frame.copy(), detections)
        return annotated, detections

    def stream_base64(self) -> Generator:
        """Yield base64 frames for WebSocket streaming"""
        self.start()
        try:
            while self.is_running:
                frame, detections = self.get_frame_with_detections()
                if frame is None:
                    break
                b64 = self.detector.frame_to_base64(frame)
                yield {
                    "frame": b64,
                    "detections": detections,
                    "people_count": len(detections)
                }
        finally:
            self.stop()