import logging
import os
import uuid
from io import BytesIO
from typing import Optional

import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings

logger = logging.getLogger(__name__)


class CloudStorageService:
    def __init__(self):
        self.provider = settings.STORAGE_PROVIDER.lower()
        self.bucket_name = settings.AWS_BUCKET_NAME
        self.client = None

        if self.provider in ["s3", "r2"]:
            if not self.bucket_name:
                logger.warning("AWS_BUCKET_NAME is not set, cloud storage may fail.")

            endpoint_url = None
            if self.provider == "r2":
                if not settings.R2_ACCOUNT_ID:
                    logger.warning("R2_ACCOUNT_ID is not set for Cloudflare R2.")
                else:
                    endpoint_url = (
                        f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
                    )

            self.client = boto3.client(
                "s3",
                endpoint_url=endpoint_url,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION if settings.AWS_REGION else "auto",
            )
        elif self.provider == "local":
            logger.info("Storage provider is set to local. S3 client not initialized.")
        else:
            logger.error(f"Unknown storage provider: {self.provider}")

    def _validate_file(self, file: UploadFile) -> None:
        """Validate file size and type."""
        # Validate content type
        allowed_types = [t.strip() for t in settings.ALLOWED_IMAGE_TYPES.split(",")]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file.content_type} is not allowed. Allowed types: {settings.ALLOWED_IMAGE_TYPES}",
            )

        # File size is often validated stream-side in FastAPI, but if we need strict validation:
        # We can check file.size if provided, or rely on nginx/fastapi middleware for MAX_UPLOAD_SIZE_MB
        if file.size and file.size > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size exceeds maximum limit of {settings.MAX_UPLOAD_SIZE_MB}MB",
            )

    def upload_file(self, file: UploadFile, directory: str = "general") -> str:
        """
        Upload a file to the configured storage provider.
        Returns the generated path/key of the file.
        """
        self._validate_file(file)

        if self.provider == "local":
            # For local fallback if needed (e.g. testing without mocks)
            os.makedirs(os.path.join(settings.UPLOAD_DIR, directory), exist_ok=True)
            ext = os.path.splitext(file.filename)[1] if file.filename else ""
            filename = f"{uuid.uuid4().hex}{ext}"
            file_path = os.path.join(settings.UPLOAD_DIR, directory, filename)

            with open(file_path, "wb") as buffer:
                buffer.write(file.file.read())

            return f"{directory}/{filename}"

        if not self.client:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Cloud storage client is not properly initialized.",
            )

        # Generate unique filename
        ext = os.path.splitext(file.filename)[1] if file.filename else ""
        filename = f"{uuid.uuid4().hex}{ext}"
        object_name = f"{directory}/{filename}"

        try:
            file_bytes = file.file.read()
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=file_bytes,
                ContentType=file.content_type,
            )
            return object_name
        except ClientError as e:
            logger.error(f"Error uploading file to {self.provider}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload file to cloud storage.",
            )

    def generate_presigned_url(self, object_name: str, expiration: int = 3600) -> str:
        """
        Generate a presigned URL to share an S3 object.
        """
        if self.provider == "local":
            if settings.CDN_BASE_URL:
                return f"{settings.CDN_BASE_URL}/{object_name}"
            return f"/static/uploads/{object_name}"

        if not self.client:
            return ""

        try:
            response = self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": object_name},
                ExpiresIn=expiration,
            )
            return response
        except ClientError as e:
            logger.error(f"Error generating presigned URL: {e}")
            return ""

    def delete_file(self, object_name: str) -> bool:
        """
        Delete a file from the configured storage provider.
        """
        if self.provider == "local":
            file_path = os.path.join(settings.UPLOAD_DIR, object_name)
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False

        if not self.client:
            return False

        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=object_name)
            return True
        except ClientError as e:
            logger.error(f"Error deleting file from {self.provider}: {e}")
            return False


storage_service = CloudStorageService()
