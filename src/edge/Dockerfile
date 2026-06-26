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
COPY cliff.py .
COPY direction_decision.py .
COPY vitesse_decision.py .

# Spécifier la commande pour exécuter le script Python
CMD ["python", "main.py"]
