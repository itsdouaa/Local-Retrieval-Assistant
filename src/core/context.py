import embeddings
import history
from database import Database

def retrieve(question, opened_db: Database = None):
    if not opened_db:
        return ""
    
    context_parts = []
    
    try:
        question_embeddings = embeddings.generate(question)
        if not question_embeddings:
            return ""
        
        embeddings_table = opened_db.get_table("embeddings")
        if not embeddings_table:
            return ""
        
        retrieved_results = embeddings_table.search_similar([question_embeddings])
        if not retrieved_results:
            return ""
        
        embeddings_message_table = opened_db.get_table("embeddings_message")
        history_table = opened_db.get_table("history")
        
        if not embeddings_message_table or not history_table:
            return ""
        
        messages_ids = []
        for result in retrieved_results:
            rows = embeddings_message_table.select(
                ["message_id"], 
                "embedding_rowid == ?", 
                [result]
            )
            if rows:
                messages_ids.append(rows[0][0])
        
        for message_id in messages_ids:
            rows = history_table.select(
                ["content"], 
                "id = ?", 
                [message_id]
            )
            if rows:
                context_parts.append(rows[0][0])
    
    except Exception:
        return ""
    
    return "\n\n".join(context_parts)
