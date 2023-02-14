# Définir l'image de base
FROM python:3.11.0

# Définir le répertoire de travail de l'application
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY . /app

# Installer les dépendances de l'application
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 5000 pour accéder à l'application
EXPOSE 5000

# Lancer l'application
CMD [ "python", "app.py" ]




