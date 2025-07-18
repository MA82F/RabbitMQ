from typing import Optional
import os
from datetime import datetime

from ..domain.entities import ImageProcessingTask, ProcessingResult, ProcessingStatus
from ..domain.interfaces import IImageProcessor, IFileStorage, IMessagePublisher


class ImageProcessingService:
    """Use Case برای پردازش تصویر"""
    
    def __init__(
        self,
        image_processor: IImageProcessor,
        file_storage: IFileStorage,
        message_publisher: IMessagePublisher
    ):
        self._image_processor = image_processor
        self._file_storage = file_storage
        self._message_publisher = message_publisher

    def process_image_task(self, image_path: str) -> ProcessingResult:
        """پردازش کامل یک تسک تصویر"""
        
        # ایجاد تسک جدید
        task = ImageProcessingTask(
            image_path=image_path,
            created_at=datetime.now()
        )
        
        try:
            print(f"🖼 starting process...: {image_path}")
            
            # شروع پردازش
            task.mark_as_processing()
            
            # پردازش تصویر
            output_path = self._image_processor.process(image_path)
            
            # آپلود فایل پردازش شده
            upload_success = self._file_storage.upload_file(output_path, output_path)
            
            if upload_success:
                task.mark_as_success(output_path)
                print(f"✅ proccessed successfully: {output_path}")
                
                result = ProcessingResult(
                    filename=os.path.basename(image_path),
                    status=ProcessingStatus.SUCCESS,
                    output_path=output_path
                )
            else:
                raise Exception("خطا در آپلود فایل")
                
        except Exception as e:
            error_msg = str(e)
            task.mark_as_failed(error_msg)
            print(f"❌ failure in proccessing: {error_msg}")
            
            result = ProcessingResult(
                filename=os.path.basename(image_path),
                status=ProcessingStatus.FAILED,
                error_message=error_msg
            )
        
        # ارسال نتیجه
        self._message_publisher.publish_result(result)
        
        return result
