import requests
import threading

# URL de l'endpoint du formulaire de contact
url = "http://127.0.0.1:5000/contact"

# Données à envoyer dans le formulaire de contact
data = {
    "name": "DIALLO Aissatou",
    "email": "aissatou@gmail.com",
    "message": "Message malveillant"
}

# Nombre de requêtes à envoyer
num_requests = 100

# Fonction pour envoyer des requêtes POST
def send_request():
    try:
        response = requests.post(url, data=data)
        print(f"Statut de la réponse : {response.status_code}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de la requête : {e}")

# Envoyer de manière simultanée des requêtes POST multiples
threads = []
for _ in range(num_requests):
    thread = threading.Thread(target=send_request)
    thread.start()
    threads.append(thread)

# Attendre que toutes les requêtes soient terminées
for thread in threads:
    thread.join()

print("Toutes les requêtes ont été envoyées.")
