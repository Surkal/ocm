## Installation

### Prérequis

*Docker* doit être installé sur votre machine

### Build de l'image docker

`docker build -t flask-ocm .`

### Lancement du serveur local 

`docker run -it --rm -p 5000:5000 ocm flask run --host=0.0.0.0`

### Njut!

Visitez => http://localhost:5000