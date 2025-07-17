from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Optional


class ProcessingStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class ImageProcessingTask:
    """Domain Entity برای پردازش تصویر"""
    image_path: str
    task_id: Optional[str] = None
    status: ProcessingStatus = ProcessingStatus.PENDING
    created_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None
    output_path: Optional[str] = None
    error_message: Optional[str] = None

    def mark_as_processing(self) -> None:
        """شروع پردازش"""
        self.status = ProcessingStatus.PROCESSING

    def mark_as_success(self, output_path: str) -> None:
        """موفقیت در پردازش"""
        self.status = ProcessingStatus.SUCCESS
        self.output_path = output_path
        self.processed_at = datetime.now()

    def mark_as_failed(self, error_message: str) -> None:
        """شکست در پردازش"""
        self.status = ProcessingStatus.FAILED
        self.error_message = error_message
        self.processed_at = datetime.now()


@dataclass
class ProcessingResult:
    """نتیجه پردازش تصویر"""
    filename: str
    status: ProcessingStatus
    output_path: Optional[str] = None
    error_message: Optional[str] = None
