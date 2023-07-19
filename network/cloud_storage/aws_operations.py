import os
import sys
from network.exception import NetworkException


class S3Sync:
    def sync_folder_to_s3(
        self, folder: str, bucket_name: str, bucket_folder_name: str
    ) -> None:
        try:
            os.system(f"aws s3 sync {folder} s3://{bucket_name}/{bucket_folder_name}/ ")

        except Exception as e:
            raise NetworkException(e, sys)

    def sync_folder_from_s3(
        self, folder: str, bucket_name: str, bucket_folder_name: str
    ) -> None:
        try:
            os.system(f"aws s3 sync s3://{bucket_name}/{bucket_folder_name}/ {folder} ")

        except Exception as e:
            raise NetworkException(e, sys)
