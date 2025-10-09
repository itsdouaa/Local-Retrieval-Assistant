# Paramètres Personnalisés

Ce guide explique comment personnaliser les paramètres du Local-Retrieval-Assistant selon vos besoins.

## 📋 Vue d'ensemble des Paramètres

### Paramètres Modifiables par Catégorie :
- 🔧 **Performances** : Modèles, embeddings, cache
- 📊 **Récupération** : Nombre de résultats, similarité
- 🏷️ **Traitement** : stopwords, langues
- 💾 **Stockage** : Base de données, fichiers temporaires
- 🎨 **Interface** : Affichage, verbosité

## 🔧 Paramètres de Performance

### Modèle d'Embedding
Modifiez : 
    `src_common/context.py`

``python
#### Changer le modèle d'embedding (ligne 15)
model = SentenceTransformer("all-MiniLM-L6-v2")  # ← Modifier ici

#### Modèles disponibles :
- "all-MiniLM-L6-v2" (par défaut, rapide, 384 dimensions)
- "all-mpnet-base-v2" (plus lent mais plus précis, 768 dimensions)
- "multi-qa-mpnet-base-dot-v1" (optimisé pour Q&A)
- "paraphrase-multilingual-MiniLM-L12-v2" (multilingue avancé)

### Taille du Cache d'Embeddings
Ajouter dans context.py

-----------------------------------------------------------------------------------------------------------------------------------------------------
import os
os.environ["TRANSFORMERS_CACHE"] = "/chemin/vers/ton/cache"  #### Linux
#### ou
os.environ["TRANSFORMERS_CACHE"] = "C:\\chemin\\vers\\ton\\cache"  #### Windows

-----------------------------------------------------------------------------------------------------------------------------------------------------

## 📊 Paramètres de Récupération

### Nombre de Résultats Récupérés
Modifiez src_common/context.py

-----------------------------------------------------------------------------------------------------------------------------------------------------
def embeddings(question):

    # ... code existant ...
    
    # Modifier le nombre de résultats (ligne ~40)
    _, indices = index.search(np.array([question_embedding]), 3)  # ← Changer 3 en 5, 10, etc.
    
    # Recommandations :
    # - 3-5 : Pour des réponses rapides et précises
    # - 5-10 : Pour une couverture plus large
    # - 10+ : Pour la recherche exhaustive (plus lent)
    
-----------------------------------------------------------------------------------------------------------------------------------------------------
### Seuil de Similarité

-----------------------------------------------------------------------------------------------------------------------------------------------------
def embeddings(question):

    # ... code existant ...
    
    # Ajouter un seuil de similarité
    distances, indices = index.search(np.array([question_embedding]), 10)
    
    # Filtrer par seuil de similarité
    similarity_threshold = 0.7  # ← Ajuster entre 0.5 et 0.9
    selected_indices = [i for i, dist in enumerate(distances[0]) 
                       if 1 - dist > similarity_threshold]
    
    selected = [contents[i] for i in selected_indices if i < len(contents)]

-----------------------------------------------------------------------------------------------------------------------------------------------------

## 🏷️ Paramètres de Traitement

### Génération de Tags
Modifiez [OS]/src/Tags.py :
-----------------------------------------------------------------------------------------------------------------------------------------------------
def get(text):

    # ... code existant ...
    
    # Modifier la longueur minimale des mots (ligne ~25)
    filtered_words = [
        word for word in words 
        if word not in all_stopwords and len(word) > 3  # ← Changer 3 en 2, 4, etc.
    ]
    
    # Modifier le nombre de tags générés
    common_words = Counter(filtered_words).most_common(20)  # ← Changer 20 en 10, 30, etc.

-----------------------------------------------------------------------------------------------------------------------------------------------------

### Langues Supportées pour l'OCR
Les langues Tesseract peuvent être ajustées dans les scripts de setup :

-----------------------------------------------------------------------------------------------------------------------------------------------------
#### Pour ajouter des langues, modifier les scripts setup.sh
sudo apt install tesseract-ocr-ara tesseract-ocr-fra tesseract-ocr-eng tesseract-ocr-spa tesseract-ocr-deu

#### ou pour Fedora
sudo dnf install tesseract-langpack-ara tesseract-langpack-fra tesseract-langpack-eng tesseract-langpack-spa tesseract-langpack-deu

-----------------------------------------------------------------------------------------------------------------------------------------------------

Puis modifier src_common/file_to_dict.py :

-----------------------------------------------------------------------------------------------------------------------------------------------------
def image(file_path):

    # ... code existant ...
    text = pytesseract.image_to_string(image, lang="eng+fra+ara+spa+deu")  # ← Ajouter langues
    
-----------------------------------------------------------------------------------------------------------------------------------------------------

## 💾 Paramètres de Stockage

### Emplacement de la Base de Données
Modifiez [OS]/src/db.py :

-----------------------------------------------------------------------------------------------------------------------------------------------------
def get_db_path():

    """Personnaliser l'emplacement de la BDD"""
    # Défaut : dans le dossier du projet
    default_path = os.path.join(os.path.dirname(__file__), "test.db")
    
    # Utiliser une variable d'environnement pour override
    custom_path = os.getenv('RETRIEVAL_DB_PATH', default_path)
    return custom_path

def save(data):

    db_path = get_db_path()  # ← Utiliser la fonction personnalisée
    # ... reste du code ...
-----------------------------------------------------------------------------------------------------------------------------------------------------

### Taille Maximale des Fichiers
Ajouter dans src_common/file_loader.py :

-----------------------------------------------------------------------------------------------------------------------------------------------------
def main():

    # ... code existant ...
    
    # Vérifier la taille du fichier
    max_file_size = 50 * 1024 * 1024  # 50MB par défaut
    file_size = os.path.getsize(file_path)
    
    if file_size > max_file_size:
        print(f"⚠️  Fichier trop volumineux ({file_size//1024//1024}MB > {max_file_size//1024//1024}MB)")
        return None

-----------------------------------------------------------------------------------------------------------------------------------------------------

## 🎨 Paramètres d'Interface

### Mode Verbose
Modifiez src_common/engine.py :

-----------------------------------------------------------------------------------------------------------------------------------------------------
def engine():

    # Ajouter en début de fonction
    verbose = True  # ← Changer en False pour moins de logs
    
    question = input("Ask Your Question : \n")
    
    while question.lower() != "exit":
        ctx = context.manager(question)
    
        prompt = f"""### Context: \n{ctx}\n### Question: {question}\n### Answer:"""
        
        if verbose:
            print("\n\n-------------------------context-------------------------\n\n", ctx)
    
        print("\n\n-------------------------response-------------------------\n\n")
        # ... reste du code ...

-----------------------------------------------------------------------------------------------------------------------------------------------------

### Formatage de la Réponse

-----------------------------------------------------------------------------------------------------------------------------------------------------
#### Personnaliser le prompt dans engine.py
prompt = f"""
**Contexte:**
{ctx}

**Question:**
{question}

**Réponse:**
"""  # ← Modifier le format selon vos préférences

-----------------------------------------------------------------------------------------------------------------------------------------------------

## 🔧 Configuration via Variables d'Environnement

### Fichier de Configuration Avancé
Créez un fichier config.py dans src_common/ :

-----------------------------------------------------------------------------------------------------------------------------------------------------
import os

#### Paramètres de performance
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
NUM_RESULTS = int(os.getenv('NUM_RESULTS', '3'))
SIMILARITY_THRESHOLD = float(os.getenv('SIMILARITY_THRESHOLD', '0.7'))

#### Paramètres de traitement
MIN_WORD_LENGTH = int(os.getenv('MIN_WORD_LENGTH', '3'))
MAX_TAGS = int(os.getenv('MAX_TAGS', '20'))
SUPPORTED_LANGUAGES = os.getenv('SUPPORTED_LANGUAGES', 'eng+fra+ara').split('+')

#### Paramètres de stockage
DB_PATH = os.getenv('DB_PATH', 'test.db')
MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', '52428800'))  # 50MB

#### Paramètres d'interface
VERBOSE = os.getenv('VERBOSE', 'True').lower() == 'true'

-----------------------------------------------------------------------------------------------------------------------------------------------------

## ⚙️ Exemples de Configurations Typiques

### Configuration Rapide (Défaut)

-----------------------------------------------------------------------------------------------------------------------------------------------------
#### Idéal pour les tests et développement
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
NUM_RESULTS = 3
VERBOSE = True

-----------------------------------------------------------------------------------------------------------------------------------------------------

### Configuration Production

-----------------------------------------------------------------------------------------------------------------------------------------------------
#### Optimisée pour la performance
EMBEDDING_MODEL = "all-mpnet-base-v2"
NUM_RESULTS = 5
SIMILARITY_THRESHOLD = 0.8
VERBOSE = False
MAX_FILE_SIZE = 104857600  # 100MB

-----------------------------------------------------------------------------------------------------------------------------------------------------

### Configuration Recherche Approfondie

-----------------------------------------------------------------------------------------------------------------------------------------------------
#### Pour une couverture maximale
EMBEDDING_MODEL = "multi-qa-mpnet-base-dot-v1"
NUM_RESULTS = 10
SIMILARITY_THRESHOLD = 0.6
MAX_TAGS = 30
-----------------------------------------------------------------------------------------------------------------------------------------------------

## 🔍 Validation des Paramètres

### Script de Vérification
Créez check_config.py :

-----------------------------------------------------------------------------------------------------------------------------------------------------
from config import *

def validate_config():

    print("🔧 Validation de la configuration...")
    
    #### Vérifier les paramètres numériques
    assert NUM_RESULTS > 0, "NUM_RESULTS doit être positif"
    assert 0 <= SIMILARITY_THRESHOLD <= 1, "SIMILARITY_THRESHOLD doit être entre 0 et 1"
    assert MIN_WORD_LENGTH >= 1, "MIN_WORD_LENGTH doit être au moins 1"
    
    print("✅ Configuration valide")
    
if __name__ == "__main__":

    validate_config()
-----------------------------------------------------------------------------------------------------------------------------------------------------

## 📝 Bonnes Pratiques

1. Testez les changements progressivement
2. Sauvegardez la configuration par défaut
3. Documentez vos modifications
4. Utilisez Git pour suivre les changements
5. Profilez les performances après modifications

## 🚀 Prochaines Étapes

1. Configuration de la Base de Données
2. Guide d'Installation
3. Dépannage

Note : Redémarrez l'application après toute modification de configuration.
