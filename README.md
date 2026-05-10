# Lab1 Docker + MinIO — Projet EFM

Ce dépôt contient une application minimale pour démontrer l'utilisation de MinIO (S3 compatible) avec une application Flask, déployée via Docker Compose.

Prérequis
- Docker et Docker Compose installés

Démarrage rapide

```bash
docker-compose build
docker-compose up -d
./scripts/init-minio.sh
```

Ouvrez http://localhost pour accéder à l'interface d'upload.

Rapport PDF

```bash
python generate_report_pdf.py
```

Générer la présentation

```bash
pip install -r requirements.txt
python generate_presentation.py
```

Fichiers clés
- `app.py` : API Flask
- `docker-compose.yml` : orchestration
- `scripts/init-minio.py` : création du bucket `uploads`
- `report.md` : rapport technique
- `report.pdf` : rapport final en PDF
- `generate_report_pdf.py` : générateur du rapport PDF

Livrables générés
- `presentation.pptx` : diaporama avec captures réelles
- `assets/ui-home.png` : capture de l'interface web
- `assets/gallery.png` : capture de la galerie des codes
- `report.pdf` : rapport PDF généré
