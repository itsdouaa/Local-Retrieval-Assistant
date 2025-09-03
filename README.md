# Local-Retrieval-Assistant
This is a Retrieval-Augmented Generation (RAG) system built in Python, designed to answer user questions by retrieving relevant context from a database of documents and generating answers using a Large Language Model (LLAMA 4 via Groq's API).


✨ Features

Multilingual Support: Works seamlessly with Arabic, English, and French content

Multiple File Format Support: Process PDF, DOCX, TXT, DOC, and images (with OCR capabilities)

Semantic Search: Advanced embedding-based retrieval using FAISS

Easy-to-Use Interface: Simple command-line interaction

Secure API Handling: Protected API key management

Automatic Tagging: Intelligent keyword extraction from content


📦 Installation

Prerequisites and Setup
Make sure to run the script : dependencies.sh  setup.sh


🚀 Usage

Start the application:
By running the command: "python engine.py" in the installation folder

Example interaction:
---------------------------------------------------------------------
Ask Your Question: 
What are the main benefits of artificial intelligence?

Do you want to add some context/files?
yes  # (opens a file selection dialog)

... (system processes files and provides response)
---------------------------------------------------------------------


📁 Project Structure

---------------------------------------------------------------------

assistant/

├── db.py              # Database management and operations

├── groq_key.py        # Secure API key retrieval

├── groq_API.py        # Groq API integration

├── context.py         # Context management & semantic retrieval

├── file_to_dict.py    # File processing for various formats

├── file_loader.py     # GUI file selection dialog

├── Tags.py            # Automated keyword/tag generation

├── stopwords.txt      # Multilingual stop words list

├── engine.py          # Main application engine

└── requirements.txt   # Python dependencies

---------------------------------------------------------------------


🔧 Configuration

Customizing Behavior
You can customize various aspects of the system:

Modify stop words - Edit stopwords.txt to add/remove words to ignore during tagging

Change embedding model - Update the model in context.py (currently using all-MiniLM-L6-v2)

Adjust retrieval settings - Modify the number of retrieved results in context.py (currently 3)


📁 Supported File Formats

Text: .txt

Documents: .docx, .doc

PDFs: .pdf

Images: .jpg, .jpeg, .png (with OCR text extraction)


🛠️ Technical Details

Core Technologies

Language Model: LLAMA 4 Scout 17B via Groq API

Embeddings: sentence-transformers/all-MiniLM-L6-v2

Vector Search: FAISS for efficient similarity search

Database: SQLite for content storage

OCR: Tesseract for text extraction from images

File Processing: PyMuPDF (PDFs), python-docx (DOCX), Mammoth (DOC)


⚙️ How It Works

Knowledge Base Construction: Users add documents through a graphical file dialog

Content Processing: Text is extracted, tagged, and stored in the database with embeddings

Query Processing: User questions are converted to embeddings and compared with stored content

Context Retrieval: The most relevant content is retrieved using semantic similarity

Response Generation: LLAMA 4 generates answers based on the retrieved context


📄 License

This project is licensed under the MIT License. See the LICENSE file for details.


🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

Fork the project

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request


📞 Support

If you encounter any issues or have questions:

Check the existing issues

Create a new issue with detailed information about your problem

Include steps to reproduce, expected behavior, and actual behavior


🚀 Future Enhancements

Potential improvements for future versions:

Web interface for easier interaction

Additional file format support

Batch processing of multiple files

Export functionality for conversations

User authentication and knowledge base separation

Enhanced multilingual support for more languages


Note: This application requires an internet connection to access the Groq API for processing queries.
