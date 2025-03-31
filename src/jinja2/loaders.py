from jinja2 import BaseLoader, TemplateNotFound


class S3TemplateLoader(BaseLoader):
    def __init__(self, bucket_name: str, prefix: str, s3_client):
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.prefix = prefix

    def get_source(self, environment, template):
        file_key = f"{self.prefix}/{template}"
        try:
            obj = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_key)
            source = obj["Body"].read().decode("utf-8")
            return source, file_key, lambda: False
        except self.s3_client.exceptions.NoSuchKey:
            raise TemplateNotFound(template)
