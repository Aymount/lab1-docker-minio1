from flask import Flask, request, jsonify, render_template_string
import boto3
import os

app = Flask(__name__)

s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("MINIO_ENDPOINT", "http://minio:9000"),
    aws_access_key_id=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
    aws_secret_access_key=os.getenv("MINIO_SECRET_KEY", "minioadmin")
)

BUCKET = os.getenv("MINIO_BUCKET", "uploads")

@app.route("/")
def index():
    return render_template_string(open("index.html").read())

@app.route("/api/files")
def list_files():
    resp = s3.list_objects_v2(Bucket=BUCKET)
    files = [o["Key"] for o in resp.get("Contents", [])]
    return jsonify({"files": files})

@app.route("/api/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "Aucun fichier fourni"}), 400
    s3.upload_fileobj(file, BUCKET, file.filename)
    return jsonify({"message": f"{file.filename} uploadé avec succès"})

@app.route("/api/delete/<filename>", methods=["DELETE"])
def delete(filename):
    s3.delete_object(Bucket=BUCKET, Key=filename)
    return jsonify({"message": f"{filename} supprimé"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)