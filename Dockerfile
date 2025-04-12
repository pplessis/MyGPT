# Définition de la base d'image
FROM python:3.9-slim

# Installation des dépendances
RUN pip install -r requirements.txt

# Copie des fichiers source dans le conteneur
COPY . /app/

# Configuration de la base de données (si nécessaire)
ENV DATABASE_URL="postgresql://user:password@db:5432/dbname"

# Exécution du script d'initialisation de la base de données (si nécessaire)
RUN python manage.py migrate

# Définition des ports à utiliser
EXPOSE 80

# Command pour lancer le serveur Web
CMD ["python", "app.py"]