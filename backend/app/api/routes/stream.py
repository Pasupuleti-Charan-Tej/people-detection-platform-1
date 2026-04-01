from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json
import logging
from app.ai.detector import WebcamStream

router = APIRouter()
logger = logging.getLogger(__name__)

@router.websocket("/ws/stream")
async def webcam_stream(websocket: WebSocket):
    """Stream live webcam detection via WebSocket"""
    await websocket.accept()
    logger.info("WebSocket client connected")
    stream = WebcamStream(camera_index=0)
    stream.start()

    try:
        while True:
            # Run detection in thread so it doesn't block
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(
                None,
                stream.get_frame_with_detections
            )
            frame, detections = data

            if frame is None:
                break

            # Convert frame to base64
            b64 = stream.detector.frame_to_base64(frame)

            # Send to frontend
            await websocket.send_text(json.dumps({
                "frame": b64,
                "detections": detections,
                "people_count": len(detections),
                "camera": "CAM-01"
            }))

            # 15fps = ~67ms per frame
            await asyncio.sleep(0.067)

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"Stream error: {e}")
    finally:
        stream.stop()