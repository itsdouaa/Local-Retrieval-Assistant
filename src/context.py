import file
import embeddings
import history
from database import Database, Virtual_Table 

def retrieve(question, opened_db: Database = None):
    context = ""
    if opened_db:
        question_embeddings = embeddings.generate(question)
        retrieved_results = opened_db.get_table("embeddings").search_similar([question_embeddings.tobytes()])
        #prochainement traitement de résultats
        #retrieved_text = ...
    added_context = query()
    context += added_context #+ retrieved_text
    return context
    
def query():
    added_context: str = ""
    add_file = {"yes": file.load, "y": file.load}
    add = add_file.get(input("do you want to add some context/files ?\n").lower())
    while add:
        added_context += add()
        add = add_file.get(input("do you want to add some context/files ?\n").lower())
    return added_context
