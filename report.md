# Rapport technique — Projet EFM (lab1-docker-minio)

Date: 10 mai 2026

## Objectif

Mettre en place une application minimale permettant d'uploader des fichiers vers MinIO (S3 compatible) via une application Flask, déployée avec Docker Compose et exposée derrière Nginx.

## Composants fournis

- `docker-compose.yml` : orchestre `minio`, `app` (Flask) et `nginx`.
- `Dockerfile` : image pour l'application Flask.
- `app.py` : API Flask — upload et liste des objets.
- `index.html` : interface simple d'upload.
- `scripts/init-minio.py` : script Python pour créer le bucket `uploads`.
- `generate_presentation.py` : script pour générer `presentation.pptx`.

## Étapes réalisées

1. Création d'une image applicative Python avec `gunicorn`.
2. Intégration du client `minio` pour interagir avec le service MinIO.
3. Ajout d'une interface HTML simple pour les tests manuels.
4. Script d'initialisation du bucket pour automatiser la création du bucket `uploads`.
5. Configuration Nginx en reverse-proxy vers le service Flask.
6. Script de génération d'une présentation sommaire en PPTX.

## Instructions d'exécution

1. Construire et démarrer les services :

```bash
docker-compose build
docker-compose up -d
```

2. Initialiser le bucket MinIO (depuis la racine du projet) :

```bash
./scripts/init-minio.sh
```

3. Ouvrir l'interface : `http://localhost` (port 80). L'application Flask est aussi accessible sur `http://localhost:5000`.

4. Générer la présentation (dans le conteneur `app` ou en local après avoir installé `requirements.txt`) :

```bash
python generate_presentation.py
```

## Prochaines améliorations possibles

- Ajouter authentification pour MinIO et l'interface.
- Gérer les pré-signed URLs pour téléchargement direct.
- Tests automatisés et CI.

## Captures du projet

![Interface web](assets/ui-home.png)

![Captures des fichiers du projet](assets/gallery.png)

