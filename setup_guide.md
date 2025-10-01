# Guide d'Installation - Local Retrieval Assistant
# ==============================================

## 📋 Prérequis Système

### Pour toutes les plateformes:
- Python 3.8 ou supérieur
- Connexion Internet (pour l'API Groq)
- Clé API Groq (obtenez-la sur https://console.groq.com/)

### Spécificités par plateforme:
- 🐧 Linux: Accès sudo pour l'installation des dépendances
- 🪟 Windows: PowerShell 5.0+ ou CMD

## 🚀 Installation Rapide

### Option 1: Installation Automatique (Recommandée)

Choisissez votre plateforme et exécutez UN SEUL script:

#### Pour Fedora:
```bash
cd Fedora/scripts
chmod +x setup.sh
./setup.sh
```
#### Pour Ubuntu:
```bash
cd Ubuntu/scripts
chmod +x setup.sh
./setup.sh
```
#### Pour Windows:
- PowerShell: Exécutez `setup.ps1`
- CMD: Double-cliquez sur `setup.bat`

### Option 2: Installation Manuelle
Si vous préférez une installation étape par étape:

1. Installez Python 3.8+ si ce n'est pas déjà fait
2. Clonez le repository
3. Choisissez votre dossier plateforme (Fedora/Ubuntu/Windows)
4. Créez l'environnement virtuel:
```bash
python -m venv venv
```
5. Activez l'environnement:
   - Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
6. Installez les dépendances:
```bash
pip install -r requirements.txt
```
7. Configurez la clé API (voir section suivante)

## 🔑 Configuration de la Clé API

### Méthode Automatique:
- Lancez le script de setup, il vous demandera votre clé API
- La clé sera stockée automatiquement au bon emplacement

### Méthode Manuelle:
- Sur Linux:
```bash
echo "votre_clé_api_ici" | sudo tee /etc/groq_API.txt
sudo chmod 600 /etc/groq_API.txt
```
- Sur Windows:
  - Créez un fichier `groq_API.txt` dans le dossier `Windows/src/` avec votre clé API.

## ✅ Vérification de l'Installation
Après l'installation, testez que tout fonctionne:
```bash
cd src/
python -c "import groq_API; print('✓ API configurée')"
python -c "import db; print('✓ Base de données OK')"
```

## 🐛 Dépannage Rapide

### Problèmes Courants:
- **Erreur de permissions:**
  - Linux: Utilisez `sudo` ou vérifiez les permissions
  - Windows: Exécutez PowerShell en tant qu'administrateur

- **Clé API introuvable:**
  - Vérifiez que le fichier `groq_API.txt` existe au bon emplacement
  - Vérifiez que la clé est correctement formatée

- **Dépendances manquantes:**
  - Réexécutez le script de setup
  - Ou exécutez: `pip install -r requirements.txt`

- **Problèmes Tesseract (OCR):**
  - Linux: `sudo apt install tesseract-ocr` ou `sudo dnf install tesseract`
  - Windows: Le script l'installe automatiquement via Chocolatey

## 📖 Documentation Complète
Pour plus de détails, consultez les guides détaillés dans:
- `/docs/installation/` → Guides d'installation complets
- `/docs/troubleshooting/` → Solutions aux problèmes spécifiques
- `/docs/configuration/` → Configuration avancée

## 🆘 Support
Si vous rencontrez des problèmes:
1. Consultez d'abord la documentation dans `/docs/troubleshooting/`
2. Vérifiez les issues existantes sur GitHub
3. Créez une nouvelle issue avec:
   - Votre plateforme et version OS
   - Les étapes exactes pour reproduire le problème
   - Les messages d'erreur complets

## 🔄 Mise à Jour
Pour mettre à jour vers une nouvelle version:
1. Sauvegardez votre base de données `test.db` si importante
2. Récupérez la dernière version: `git pull origin main`
3. Réexécutez le script de setup de votre plateforme
4. Restorez votre base de données si nécessaire

## ⚠️ Notes Importantes
- Cette application nécessite une connexion Internet active
- La première exécution peut prendre du temps (téléchargement des modèles)
- Les fichiers traités sont stockés dans la base de données SQLite
- La performance dépend de la puissance de votre machine et de la connexion Internet
