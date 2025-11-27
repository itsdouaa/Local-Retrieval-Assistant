import embeddings
import history
from database import Database, Virtual_Table 
from attempts import Attempt

attempt = Attempt()

def retrieve(question, opened_db: Database = None):
    context = ""
    if not opened_db:
        return context
        
    question_embeddings = embeddings.generate(question)
    retrieved_results = opened_db.get_table("embeddings").search_similar([question_embeddings])
    if retrieved_results:
        messages_ids = []
        for result in retrieved_results:
            if opened_db.get_table("embeddings_message").select(["message_id"], "embedding_rowid == ?", [result]):
                messages_ids.append(opened_db.get_table("embeddings_message").select(["message_id"], "embedding_rowid == ?", [result])[0][0])
        for _id in messages_ids:
            message = opened_db.get_table("history").select(["content"], "id = ?", [_id])[0][0]
            print(message)
            context += message + "\n\n"
    #except Exception as e:
        #print(f"Erreur lors de la récupération: {e}")
        #context = ""
    
    print(f"\n\n context : \n{context}\n\n")
    return context.strip()

