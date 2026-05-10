import os
import time
from minio import Minio

endpoint = os.environ.get('MINIO_ENDPOINT', 'localhost:9000')
access = os.environ.get('MINIO_ACCESS_KEY', 'minioadmin')
secret = os.environ.get('MINIO_SECRET_KEY', 'minioadmin')
bucket = os.environ.get('MINIO_BUCKET', 'uploads')

client = Minio(endpoint, access_key=access, secret_key=secret, secure=False)

for i in range(20):
    try:
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)
        print('Bucket ready:', bucket)
        break
    except Exception as e:
        print('Waiting for MinIO...', e)
        time.sleep(2)
