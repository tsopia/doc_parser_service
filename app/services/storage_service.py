import boto3
import tempfile
import os

class StorageService:
    """封装从对象存储（S3/OSS）下载文件的能力"""

    def __init__(self, endpoint_url=None, bucket_name=None, access_key=None, secret_key=None):
        self.s3 = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        self.bucket = bucket_name

    def download_file(self, object_key: str) -> str:
        """从对象存储下载到本地临时文件"""
        suffix = os.path.splitext(object_key)[1]
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        self.s3.download_fileobj(self.bucket, object_key, tmp)
        tmp.close()
        return tmp.name
