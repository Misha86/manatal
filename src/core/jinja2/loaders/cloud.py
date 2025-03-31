

import boto3
from jinja2 import BaseLoader, TemplateNotFound


class S3TemplateLoader(BaseLoader):
    def __init__(self, bucket_name: str, prefix: str, **params):
        self.s3 = boto3.client("s3", **params)
        self.bucket_name = bucket_name
        self.prefix = prefix

    def get_source(self, environment, template):
        file_key = f"{self.prefix}/{template}"
        try:
            obj = self.s3.get_object(Bucket=self.bucket_name, Key=file_key)
            source = obj["Body"].read().decode("utf-8")
            return source, file_key, lambda: False
        except self.s3.exceptions.NoSuchKey:
            raise TemplateNotFound(template)
