from .storages import S3Storage
from src.config import settings

class PrivateS3Storage(S3Storage):
    AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
    AWS_S3_BUCKET_NAME = settings.AWS_S3_BUCKET_NAME
    AWS_S3_ENDPOINT_URL = "s3.amazonaws.com"
    AWS_S3_USE_SSL = True
    AWS_S3_CUSTOM_DOMAIN = settings.AWS_S3_CUSTOM_DOMAIN
    
    
storage = PrivateS3Storage()