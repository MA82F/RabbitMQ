import boto3
from botocore.exceptions import ClientError
from ..domain.interfaces import IFileStorage


class MinIOStorage(IFileStorage):
    """پیاده‌سازی ذخیره فایل در MinIO"""
    
    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket: str):
        self.endpoint = endpoint
        self.bucket = bucket
        self.s3_client = boto3.client(
            's3',
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='us-east-1'
        )
    
    def get_file_url(self, remote_path: str) -> str:
        return f"{self.endpoint}/{self.bucket}/{remote_path}"

    def upload_file(self, local_path: str, remote_path: str) -> bool:
        """آپلود فایل به MinIO"""
        try:
            self.s3_client.upload_file(local_path, self.bucket, remote_path)
            print(f"✅ فایل آپلود شد به MinIO: {remote_path}")
            return True
            
        except ClientError as e:
            print(f"❌ خطا در آپلود به MinIO: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ خطای غیرمنتظره در آپلود: {str(e)}")
            return False
