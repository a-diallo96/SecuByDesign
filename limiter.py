from flask import request
from functools import wraps
from collections import defaultdict
import time

# Dictionnaire pour stocker les timestamps des requêtes par adresse IP
request_timestamps = defaultdict(list)

# Fonction pour limiter le nombre de requêtes par adresse IP dans un laps de temps donné
def limit_requests(window_size, max_requests):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            client_ip = request.remote_addr  # Obtenir l'adresse IP du client
            current_time = time.time()  # Obtenir le timestamp actuel

            # Supprimer les timestamps expirés du dictionnaire
            request_timestamps[client_ip] = [t for t in request_timestamps[client_ip] if t > current_time - window_size]

            # Vérifier si le nombre de requêtes dépasse la limite
            if len(request_timestamps[client_ip]) > max_requests:
                return "Trop de requêtes. Veuillez réessayer plus tard.", 429  # Renvoyer un code d'erreur 429 (Trop de demandes)

            # Ajouter le timestamp de la nouvelle demande à la liste
            request_timestamps[client_ip].append(current_time)

            # Appeler la fonction de vue
            return func(*args, **kwargs)
        return wrapper
    return decorator
