import embeddings
from database import Database

def save(opened_db, messages: list[dict]):
    history_table = opened_db.get_table("history")
    embeddings_table = opened_db.get_table("embeddings")
    embeddings_message_table = opened_db.get_table("embeddings_message")
    for message in messages:
        message_record = list(message.values())
        history_table.insert(message_record, ["role", "content"])
        message_id = history_table.db_cursor.lastrowid
        message_embeddings = embeddings.generate(message["content"])
        for embedding in message_embeddings:
            embeddings_table.insert([embedding])
            embedding_id = embeddings_table.db_cursor.lastrowid
            opened_db.link_tables(embeddings_message_table, [embedding_id, message_id])

