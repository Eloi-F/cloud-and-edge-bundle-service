# Utiliser une image de base Python officielle
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /cloud

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copier le fichier Python dans le conteneur
COPY main.py .
COPY identification.py .
COPY trajectory.py .
COPY coco.names .
COPY frozen_inference_graph.pb .
COPY ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt .

# Spécifier la commande pour exécuter le script Python
CMD ["python", "main.py"]
