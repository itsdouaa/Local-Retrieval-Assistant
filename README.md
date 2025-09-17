
Local-Retrieval-Assistant
Système de RAG (Retrieval-Augmented Generation) construit en Python, conçu pour répondre aux questions des utilisateurs en récupérant le contexte pertinent depuis une base de données de documents et en générant des réponses utilisant un modèle de langage large (LLAMA 4 via l'API Groq).


✨ Fonctionnalités

-Support multilingue : Fonctionne avec le contenu arabe, anglais et français
-Support multi-formats : Traite PDF, DOCX, TXT, DOC et images (avec OCR)
-Recherche sémantique : Récupération par embedding avec FAISS
-Interface simple : Interaction en ligne de commande intuitive
-Gestion sécurisée des API : Protection des clés API
-Tagging automatique : Extraction intelligente de mots-clés
-Multi-plateforme : Support complet Fedora, Ubuntu et Windows


📁 Structure du Projet

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

local_retrieval_assistant/

│

├── 📁 Fedora/                          # Version spécifique Fedora

│   ├── 📁 scripts/

│   │   └── 📄 setup.sh                 # Script d'installation unique

│   └── 📁 src/

│       ├── 📄 Tags.py                  # Génération de tags (spécifique Fedora)

│       ├── 📄 context.py               # Gestion du contexte (spécifique Fedora)

│       ├── 📄 db.py                    # Base de données (spécifique Fedora)

│       └── 📄 groq_key.py              # Lecture clé API (spécifique Fedora)

│
├── 📁 Ubuntu/                          # Version spécifique Ubuntu

│   ├── 📁 scripts/

│   │   └── 📄 setup.sh                 # Script d'installation unique

│   └── 📁 src/

│       ├── 📄 Tags.py                  # Génération de tags (spécifique Ubuntu)

│       ├── 📄 context.py               # Gestion du contexte (spécifique Ubuntu)

│       ├── 📄 db.py                    # Base de données (spécifique Ubuntu)

│       └── 📄 groq_key.py              # Lecture clé API (spécifique Ubuntu)

│

├── 📁 Windows/                         # Version spécifique Windows

│   ├── 📁 scripts/

│   │   ├── 📄 setup.ps1                # Script PowerShell

│   │   └── 📄 setup.bat                # Script CMD

│   └── 📁 src/

│       ├── 📄 Tags.py                  # Génération de tags (spécifique Windows)

│       ├── 📄 context.py               # Gestion du contexte (spécifique Windows)

│       ├── 📄 db.py                    # Base de données (spécifique Windows)

│       └── 📄 groq_key.py              # Lecture clé API (spécifique Windows)

│

├── 📁 src_common/                      # Code commun à toutes les plateformes

│   ├── 📄 engine.py                    # Moteur principal

│   ├── 📄 file_loader.py               # Chargement de fichiers

│   ├── 📄 file_to_dict.py              # Conversion fichiers→dict

│   ├── 📄 groq_API.py                  # Intégration API Groq

│   └── 📄 stopwords.txt                # Liste de mots vides

│

├── 📁 docs/                            # Documentation complète

│   ├── 📁 configuration/               # Guides de configuration

│   ├── 📁 development/                 # Développement et contribution

│   ├── 📁 examples/                    # Exemples d'utilisation

│   ├── 📁 faq/                         # Questions fréquentes

│   ├── 📁 installation/                # Guides d'installation

│   ├── 📁 platform_differences/        # Différences entre plateformes

│   ├── 📁 troubleshooting/             # Dépannage et résolution

│   ├── 📁 tutorials/                   # Tutoriels pas à pas

│   └── 📁 usage/                       # Guides d'utilisation

│

├── 📄 .gitignore

├── 📄 LICENSE

├── 📄 README.md

└── 📄 setup_guide.txt

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------


📦 Installation

Choisissez votre plateforme :

🐧 Pour Fedora :

bash
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
cd local_retrieval_assistant/Fedora/scripts
chmod +x setup.sh
./setup.sh
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
🐧 Pour Ubuntu/Debian :

bash
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
cd local_retrieval_assistant/Ubuntu/scripts
chmod +x setup.sh
./setup.sh
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
🪟 Pour Windows :

PowerShell :

powershell
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
cd local_retrieval_assistant\Windows\scripts
.\setup.ps1
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Invite de commande :

batch
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
cd local_retrieval_assistant\Windows\scripts
setup.bat
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------


🚀 Utilisation

Après l'installation, naviguez dans le dossier src/ de votre plateforme et lancez :

bash
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
cd ../src
python engine.py
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Exemple d'interaction :

text
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Ask Your Question: 
Quels sont les avantages principaux de l'intelligence artificielle ?

Do you want to add some context/files?
yes  # (ouvre une boîte de dialogue de sélection de fichier)

... (le système traite les fichiers et fournit une réponse)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------


🔧 Architecture Technique

Code Spécifique vs Code Commun
src_common/ : Contient le code universel (90% de l'application)
[OS]/src/ : Contient les adaptations spécifiques à chaque OS (10%)

Gestion des chemins de fichiers différents

Configuration spécifique à chaque plateforme

Optimisations performances par OS

Technologies Principales
Modèle de langage : LLAMA 4 Scout 17B via API Groq

Embeddings : sentence-transformers/all-MiniLM-L6-v2

Recherche vectorielle : FAISS pour la similarité sémantique

Base de données : SQLite pour le stockage

OCR : Tesseract pour l'extraction texte depuis images

Traitement fichiers : PyMuPDF (PDF), python-docx (DOCX), Mammoth (DOC)

Formats de Fichiers Supportés

Texte : .txt
Documents : .docx, .doc
PDFs : .pdf
Images : .jpg, .jpeg, .png (avec OCR)


📖 Documentation

La documentation complète est disponible dans le dossier docs/


🤝 Contribution

Les contributions sont les bienvenues ! Voici comment procéder :

-Forkez le projet
-Créez une branche (git checkout -b feature/ma-fonctionnalite)
-Commitez vos changements (git commit -m 'Ajout ma fonctionnalité')
-Pushez la branche (git push origin feature/ma-fonctionnalite)
-Ouvrez une Pull Request


🐛 Support

Si vous rencontrez des problèmes :

-Consultez la documentation dans docs/troubleshooting/
-Vérifiez les issues existantes sur GitHub
-Créez une nouvelle issue avec des détails complets :
    Plateforme et version OS
    Étapes pour reproduire le problème
    Messages d'erreur complets
    Comportement attendu vs observé


📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.


🚀 Améliorations Futures

-Interface web pour une interaction plus facile
-Support de formats de fichiers supplémentaires
-Traitement par lots de multiples fichiers
-Fonctionnalité d'export des conversations
-Authentification utilisateur et séparation des bases de connaissances
-Support multilingue étendu

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Note : Cette application nécessite une connexion internet pour accéder à l'API Groq.
Note : Chaque plateforme a sa version optimisée - utilisez le dossier approprié pour votre OS.
