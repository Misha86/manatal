import mimetypes
from pathlib import Path
from typing import BinaryIO

import boto3

from src.core.storages.utils import secure_filename


class BaseStorage:
    def get_name(self, name: str) -> str:
        raise NotImplementedError()

    def get_path(self, name: str) -> str:
        raise NotImplementedError()

    def get_size(self, name: str) -> int:
        raise NotImplementedError()

    def open(self, name: str) -> BinaryIO:
        raise NotImplementedError()

    def write(self, file: BinaryIO, name: str) -> str:
        raise NotImplementedError()

    def generate_new_filename(self, filename: str) -> str:
        raise NotImplementedError()


class S3Storage(BaseStorage):
    default_content_type = "application/octet-stream"

    AWS_ACCESS_KEY_ID = ""
    AWS_SECRET_ACCESS_KEY = ""
    AWS_S3_BUCKET_NAME = ""
    AWS_S3_ENDPOINT_URL = ""
    AWS_S3_USE_SSL = True
    AWS_DEFAULT_ACL = ""
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_CUSTOM_DOMAIN = ""

    def __init__(self) -> None:
        assert not self.AWS_S3_ENDPOINT_URL.startswith("http"), "URL should not contain protocol"

        self._http_scheme = "https" if self.AWS_S3_USE_SSL else "http"
        self._url = f"{self._http_scheme}://{self.AWS_S3_ENDPOINT_URL}"
        self._s3 = boto3.resource(
            "s3",
            endpoint_url=self._url,
            use_ssl=self.AWS_S3_USE_SSL,
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
        )
        self._bucket = self._s3.Bucket(name=self.AWS_S3_BUCKET_NAME)

    def get_name(self, name: str) -> str:
        filename = secure_filename(Path(name).name)
        return str(Path(name).with_name(filename))

    def get_path(self, name: str) -> str:
        """Get full URL to the file."""

        key = self.get_name(name)

        if self.AWS_S3_CUSTOM_DOMAIN:
            return f"{self._http_scheme}://{self.AWS_S3_CUSTOM_DOMAIN}/{key}"

        if self.AWS_QUERYSTRING_AUTH:
            params = {"Bucket": self._bucket.name, "Key": key}
            return self._s3.meta.client.generate_presigned_url("get_object", Params=params)

        return f"{self._http_scheme}://{self.AWS_S3_ENDPOINT_URL}/{self.AWS_S3_BUCKET_NAME}/{key}"

    def get_size(self, name: str) -> int:
        """Get file size in bytes."""

        key = self.get_name(name)
        return self._bucket.Object(key).content_length

    def write(self, file: BinaryIO, name: str) -> str:
        """Write input file which is opened in binary mode to destination."""

        file.seek(0, 0)
        key = self.get_name(name)
        content_type, _ = mimetypes.guess_type(key)
        params = {
            "ACL": self.AWS_DEFAULT_ACL,
            "ContentType": content_type or self.default_content_type,
        }
        self._bucket.upload_fileobj(file, key, ExtraArgs=params)
        return self.get_path(key)

    def delete(self, name: str) -> None:
        key = self.get_name(name)
        self._bucket.Object(key).delete()

    def generate_new_filename(self, filename: str) -> str:
        key = self.get_name(filename)
        stem = Path(filename).stem
        suffix = Path(filename).suffix
        counter = 0

        while self._check_object_exists(key):
            counter += 1
            filename = f"{stem}_{counter}{suffix}"
            key = self.get_name(filename)

        return filename

    def _check_object_exists(self, key: str) -> bool:
        try:
            self._bucket.Object(key).load()
        except boto3.exceptions.botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False

        return True
