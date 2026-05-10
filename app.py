import os
import tempfile
from pathlib import Path

from flask import Flask, request, redirect, url_for, send_from_directory, jsonify
from minio import Minio
from minio.error import S3Error

app = Flask(__name__, static_folder='')

MINIO_ENDPOINT = os.environ.get('MINIO_ENDPOINT', 'localhost:9000')
MINIO_ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY', 'minioadmin')
MINIO_SECRET_KEY = os.environ.get('MINIO_SECRET_KEY', 'minioadmin')
BUCKET = os.environ.get('MINIO_BUCKET', 'uploads')
STORAGE_BACKEND = os.environ.get('STORAGE_BACKEND', 'minio')
LOCAL_STORAGE_DIR = Path(os.environ.get('LOCAL_STORAGE_DIR', tempfile.gettempdir())) / 'lab1-docker-minio'
PORT = int(os.environ.get('PORT', '5000'))

client = None


def get_client():
    global client
    if client is None and STORAGE_BACKEND == 'minio':
        client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False,
        )
    return client


def use_local_storage():
    return STORAGE_BACKEND == 'local'


def ensure_local_bucket():
    LOCAL_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

def ensure_bucket(bucket_name):
    if use_local_storage():
        ensure_local_bucket()
        return
    minio_client = get_client()
    try:
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
    except S3Error as e:
        app.logger.error('MinIO error: %s', e)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part', 400
    f = request.files['file']
    if f.filename == '':
        return 'No selected file', 400
    ensure_bucket(BUCKET)
    content = f.read()
    if use_local_storage():
        ensure_local_bucket()
        target = LOCAL_STORAGE_DIR / f.filename
        target.write_bytes(content)
    else:
        minio_client = get_client()
        minio_client.put_object(BUCKET, f.filename, data=content, length=len(content), content_type=f.content_type)
    return redirect(url_for('index'))

@app.route('/list')
def list_objects():
    ensure_bucket(BUCKET)
    items = []
    if use_local_storage():
        ensure_local_bucket()
        for path in sorted(LOCAL_STORAGE_DIR.iterdir()):
            if path.is_file():
                items.append({'name': path.name, 'size': path.stat().st_size})
    else:
        minio_client = get_client()
        objs = minio_client.list_objects(BUCKET, recursive=True)
        for o in objs:
            items.append({'name': o.object_name, 'size': o.size})
    return jsonify(items)

if __name__ == '__main__':
    ensure_bucket(BUCKET)
    app.run(host='0.0.0.0', port=PORT, debug=True)
