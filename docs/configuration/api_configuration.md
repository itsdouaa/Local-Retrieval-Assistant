# Configuration de l'API Groq

Ce guide explique comment configurer et gérer l'API Groq pour le Local-Retrieval-Assistant.

## 📋 Prérequis

- Un compte Groq (https://console.groq.com/)
- Une clé API Groq valide
- Python 3.8+ installé

## 🔑 Obtenir une Clé API Groq

### Étape 1: Créer un compte Groq
1. Allez sur https://console.groq.com/
2. Cliquez sur "Sign Up" et créez un compte
3. Vérifiez votre email

### Étape 2: Générer une clé API
1. Connectez-vous à votre compte Groq
2. Allez dans la section "API Keys"
3. Cliquez sur "Create API Key"
4. Donnez un nom à votre clé (ex: "local-retrieval-assistant")
5. Copiez la clé générée ⚠️ (vous ne la verrez qu'une fois)

### Étape 3: Notes de sécurité
- 🔒 Ne partagez jamais votre clé API
- 🔒 Ne commitez pas votre clé dans Git
- 🔒 Régénérez la clé si elle est compromise

## ⚙️ Configuration de la Clé API

### Méthode Automatique (Recommandée)

Lancez le script de setup de votre plateforme :

# Fedora/Ubuntu (bash)
cd scripts/
./setup.sh

# Windows (PowerShell)
.\setup.ps1

# Windows (CMD)
setup.bat

Le script vous demandera votre clé API et la configurera automatiquement.

### Méthode Manuelle

# Sur Linux :(bash)
-----------------------------------------------------------------------------------------------------------------------------------------------------
# Créer le fichier avec votre clé
echo "votre_clé_api_ici" | sudo tee /etc/groq_API.txt

# Sécuriser les permissions
sudo chmod 600 /etc/groq_API.txt

# Vérifier la configuration
sudo cat /etc/groq_API.txt
-----------------------------------------------------------------------------------------------------------------------------------------------------

# Sur Windows :

1. Créez un fichier groq_API.txt dans le dossier src/
2.Collez votre clé API dans le fichier
3.Sauvegardez le fichier

## 🔍 Vérification de la Configuration

### Test manuel :
-----------------------------------------------------------------------------------------------------------------------------------------------------
#Testez la configuration
python -c "
from groq_key import read
try:
    api_key = read()
    print('✅ Clé API configurée avec succès')
    print(f'📋 Clé: {api_key[:10]}...{api_key[-5:]}')
except Exception as e:
    print(f'❌ Erreur: {e}')
"
-----------------------------------------------------------------------------------------------------------------------------------------------------

### Test via l'application :
-----------------------------------------------------------------------------------------------------------------------------------------------------
cd src/
python -c "
import groq_API
try:
    # Test de connexion simple
    response = groq_API.ask('Test de connexion')
    print('✅ Connexion à l\'API Groq réussie')
except Exception as e:
    print(f'❌ Erreur de connexion: {e}')
"
-----------------------------------------------------------------------------------------------------------------------------------------------------

## ⚠️ Dépannage des Problèmes Courants

### Erreur: "API key not found"
Solution :
bash
-----------------------------------------------------------------------------------------------------------------------------------------------------
# Vérifiez l'emplacement du fichier
# Linux : /etc/groq_API.txt
# Windows : groq_API.txt dans le dossier src/

# Vérifiez les permissions (Linux)
ls -la /etc/groq_API.txt
-----------------------------------------------------------------------------------------------------------------------------------------------------

### Erreur: "Invalid API key"
Solution :

1. Vérifiez que la clé est correctement copiée

2. Régénérez une nouvelle clé sur https://console.groq.com/

3. Assurez-vous qu'il n'y a pas d'espaces avant/après la clé

### Erreur: "Rate limit exceeded"
Solution :

1. Attendez quelques minutes avant de réessayer

2. Vérifiez votre quota sur https://console.groq.com/

3. Passez à un plan payant si nécessaire


## 🔧 Configuration Avancée

### Changer de Modèle LLM
Modifiez groq_API.py :
-----------------------------------------------------------------------------------------------------------------------------------------------------
# Changer le modèle (options disponibles)
completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",  # ← Modifier ici
    # Autres paramètres...
)

# Modèles disponibles :
# - "meta-llama/llama-4-scout-17b-16e-instruct" (par défaut)
# - "mixtral-8x7b-32768"
# - "gemma-7b-it"
# - "llama3-70b-8192"
-----------------------------------------------------------------------------------------------------------------------------------------------------

### Paramètres d'API Avancés
-----------------------------------------------------------------------------------------------------------------------------------------------------
completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[{"role": "user", "content": prompt}],
    temperature=1,           # ← Contrôle la créativité (0-2)
    max_completion_tokens=1024,  # ← Tokens maximum en réponse
    top_p=1,                 # ← Contrôle la diversité
    stream=True,             # ← Réponse en streaming
    stop=None,               # ← Mots d'arrêt
)
-----------------------------------------------------------------------------------------------------------------------------------------------------

### Variables d'Environnement (Alternative)
Vous pouvez aussi utiliser des variables d'environnement :
-----------------------------------------------------------------------------------------------------------------------------------------------------
# Linux
export GROQ_API_KEY="votre_clé_api_ici"

# Windows (CMD)
set GROQ_API_KEY=votre_clé_api_ici

# Windows (PowerShell)
$env:GROQ_API_KEY="votre_clé_api_ici"
-----------------------------------------------------------------------------------------------------------------------------------------------------
Puis modifiez groq_key.py pour les lire :
-----------------------------------------------------------------------------------------------------------------------------------------------------
import os

def read():
    # Essayer la variable d'environnement d'abord
    api_key = os.getenv('GROQ_API_KEY')
    if api_key:
        return api_key
    
    # Sinon, utiliser le fichier
    # ... reste du code ...
-----------------------------------------------------------------------------------------------------------------------------------------------------

## 📊 Monitoring et Quotas

Vérifier l'utilisation de l'API :
1. Allez sur https://console.groq.com/

2. Cliquez sur "Usage" dans le menu

3. Consultez vos statistiques d'utilisation

Quotas par défaut :
🔹 Requêtes par minute : Variable selon le modèle

🔹 Tokens par minute : Variable selon le modèle

🔹 Modèles disponibles : Dépend de votre plan

## 🔒 Bonnes Pratiques de Sécurité
Ne jamais commiter les clés API

Utiliser des permissions restrictives (chmod 600)

Régénérer régulièrement les clés

Utiliser des clés différentes pour dev/prod

Monitorer l'utilisation pour détecter les abus

## � Support

Si vous rencontrez des problèmes :
1. Consultez https://console.groq.com/support

2. Vérifiez la documentation Groq

3. Créez une issue sur GitHub
