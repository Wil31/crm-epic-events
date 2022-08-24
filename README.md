[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

# CRM-EPIC-Events
Logiciel gestion de la relation client (CRM) de l'entreprise, qui effectue le suivi de tous les clients et événements.  
Projet 12 OC.

## Utilisation

### Prérequis

* Un terminal (par exemple Windows PowerShell)
* Python3 version >= 3.10 (vérifier avec `python -V`)

### 1 - Télécharger les fichiers

* Téléchargez depuis le lien:
  [https://github.com/.../main.zip](https://github.com/Wil31/crm-epic-events/archive/refs/heads/main.zip)
* Extraire le .zip

### 2 - Configurer l'environnement virtuel

* Ouvrez un terminal
* Naviguez vers le dossier extrait _([...]\Issue-Tracker-SoftDesk)_
* Créez un environnement virtuel avec la commande `python -m venv env`
* Activer l'environnement
  avec `.\env\Scripts\activate` (`source env/bin/activate` sur Linux)
* Installez les packages avec `pip install -r .\requirements.txt`

### 3 - Exécuter le code

* Lancez le serveur depuis le terminal avec la
  commande `py.exe manage.py runserver`
* Utilisez une application comme Postman pour communiquer avec les endpoints.

### 4 - Tester l'API

**Veuillez consulter [la documentation de l'API](https://documenter.getpostman.com/view/19642426/VUquLFQC#843d0c18-b00c-4367-ab8b-9f9fbe6674a8)
pour l'utilisation des différents endpoints.**

Créez de nouveaux utilisateurs ou utilisez les identifiants des comptes 
suivants pour essayer les endpoints de l'API.

**Compte Manager :**  
Email : `manager@user.com`  
MdP : `blagnac11`

**Compte Sales :**  
Email : `sales@user.com`  
MdP : `blagnac11`

**Compte Support :**  
Email : `support@user.com`  
MdP : `blagnac11`

**Compte superuser :**  
Email : `super@user.com`  
MdP : `super`
