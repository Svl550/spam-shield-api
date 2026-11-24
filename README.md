# SpamShield API - Guide de Mise en Ligne & Monétisation

Votre API **SpamShield** est entièrement codée, testée et prête à être monétisée sur RapidAPI.

---

## 📁 Structure du Projet
* **`main.py`** : Endpoints FastAPI (`/v1/verify`, `/v1/batch-verify`, `/health`).
* **`services/verifier.py`** : Moteur d'analyse (syntaxe RFC, serveurs MX, domaines jetables, score de risque).
* **`data/disposable_domains.py`** : Base de données de domaines de spam & temporaires.
* **`openapi.json`** : Fichier de spécification prêt à importer sur RapidAPI.
* **`render.yaml` & `Dockerfile`** : Fichiers pour hébergement gratuit en 1 clic.

---

## 🚀 Étape 1 : Héberger l'API gratuitement (3 minutes)

1. Créez un compte gratuit sur [Render.com](https://render.com) (ou [Koyeb.com](https://www.koyeb.com)).
2. Déposez ce dossier sur votre compte GitHub (en repo privé ou public).
3. Sur Render :
   * Cliquez sur **New +** > **Web Service**.
   * Sélectionnez votre dépôt GitHub.
   * Render détecte automatiquement `render.yaml` ou Python.
   * Cliquez sur **Deploy**.
4. Au bout de 2 minutes, Render vous donne l'URL publique de votre API :
   `https://spamshield-api-xxxx.onrender.com`

---

## 🌐 Étape 2 : Publier l'API sur RapidAPI (5 minutes)

1. Rendez-vous sur [rapidapi.com](https://rapidapi.com) et créez un compte gratuit.
2. Allez dans le **Provider Dashboard** (en haut à droite : *My APIs* ou *Add New API*).
3. Choisissez **Upload OpenAPI Spec** :
   * Sélectionnez le fichier `openapi.json` présent dans ce dossier.
   * RapidAPI va générer automatiquement tous les endpoints, tests et documentation !
4. Dans l'onglet **Settings / Target URL** :
   * Collez l'URL de votre API Render (ex: `https://spamshield-api-xxxx.onrender.com`).
5. Cliquez sur **Save**.

---

## 💰 Étape 3 : Configurer les Tarifs (Plans & Pricing)

Dans l'onglet **Plans & Pricing** sur RapidAPI, activez les paliers suivants (recommandés pour maximiser les conversions) :

1. **Basic (Gratuit)** :
   * Quota : 100 requêtes / mois.
   * But : Permettre aux développeurs d'essayer l'API gratuitement.
2. **Pro (14,99 $ / mois)** :
   * Quota : 10 000 requêtes / mois.
   * Dépassement : 0,002 $ / requête.
3. **Ultra (39,99 $ / mois)** :
   * Quota : 50 000 requêtes / mois.
   * Dépassement : 0,001 $ / requête.
4. **Mega (99,99 $ / mois)** :
   * Quota : 200 000 requêtes / mois.

---

## 💳 Étape 4 : Encaisser les Gains
* Dans les paramètres de votre compte RapidAPI (**Payout Settings**), renseignez simplement votre compte bancaire (IBAN) ou compte PayPal.
* RapidAPI encaisse les cartes bancaires des développeurs dans le monde entier et vous verse les fonds chaque mois automatiquement.
