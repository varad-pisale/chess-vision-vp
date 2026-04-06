# Accepts any source (IP url, 0 for webcam, a video file path)
# Exposes a consistent interface to the rest of the app — the pipeline shouldn't care where frames come from
# Handles connection, reconnection, and release

"""
camera.py
---------
Abstraction layer for all video input sources.
The pipeline never interacts with a raw VideoCapture object — only this class.
"""

import cv2
import logging

logger = logging.getLogger(__name__)


class Camera:
    """
    Manages video input from any source (IP webcam, USB camera, video file).
    Supports priority-based source fallback and context manager usage.

    Usage:
        with Camera(sources=["http://192.168.1.5:8080/video", 0]) as cam:
            ret, frame = cam.read()
    """

    def __init__(self, sources: list, retry_limit: int = 3):
        """
        Store configuration. Do NOT connect here.

        Args:
            sources     : Ordered list of sources to try (URL, int index, or file path)
            retry_limit : How many times to retry a dropped frame before signalling failure
        """
        self.cap = None
        self.sources = sources
        self.retry_limit = retry_limit
        self.active_source = None

    def connect(self) -> bool:
        """
        Try each source in priority order until one opens successfully.

        Returns:
            True if a source opened, False if all failed.
        """
        for s in self.sources:
            self.cap = cv2.VideoCapture(s)
            if self.cap.isOpened():
                self.active_source = s
                logger.info(f"Camera connected: {s}")
                return True
        logger.error("All sources failed")
        return False

    def read(self):
        """
        Pull one frame from the active source.
        Retries on transient glitches up to retry_limit.

        Returns:
            (True, frame)  on success
            (False, None)  on failure / source lost
        """
        if self.is_opened():
            for _ in range(self.retry_limit):
                ret, frame = self.cap.read()
                if ret:
                    return (True, frame)
        return (False, None)

    def is_opened(self) -> bool:
        """
        Check if the current source is still alive.

        Returns:
            True if connection is active, False otherwise.
        """
        return self.cap is not None and self.cap.isOpened()

    def release(self):
        """
        Gracefully close the video source and free resources.
        Safe to call even if never connected.
        """
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def __enter__(self):
        """Called at start of `with` block. Triggers connect."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called at end of `with` block (even on crash). Triggers release."""
        self.release()