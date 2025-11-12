import logging
import groq_API
import context
import embeddings
import database

def select_db():
    choice = {"1": database.create, "2": database.open_existing}
    choosen = choice.get(input("Choose an option: \n1. Create database\n2. Open existing database\n"))
    tries = 0
    while not choosen and tries < 3:
        tries += 1
        print("Invalid Option!\n")
        choosen = choice.get(input("Choose an option: \n1. Create database\n2. Open existing database\n"))
    if tries ==3:
        print("No database selected! Session cannot be started.")
        return None
        
    db_path = choosen()
    tries = 0
    while not db_path and tries < 3:
        print("You have to choose a database to continue!")
        db_path = choosen()
    if tries ==3:
        print("No database selected! Session cannot be started.")
        return None
    return db_path

def get_prompt():
    question = input("Ask Your Question : \n")
    context = context.retrieve(question)
    #print("\n\n-------------------------context-------------------------\n\n", ctx)
    if question.lower() != "exit":
        prompt = f"""### Context: \n{context}\n### Question: {question}\n### Answer:"""
    else prompt = "exit"
    
    return prompt

def start():
    db_path = select_db()
    if not db_path:
        return None
    messages = []
    prompt = get_prompt()
    while prompt != "exit":
        messages.append({"role": "user", "content": prompt})
        
        print("\n\n-------------------------response-------------------------\n\n")
        try:
            completion = groq_API.response(messages)
            full_reply = ""
            for chunk in completion:
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
                full_reply += content
            messages.append({"role": "assistant", "content": full_reply})
        except Exception as e:
            print(f"Error Connecting to API: {e}")
        
        print("\n\n-------------------------prompt-------------------------\n\n")
        prompt = get_prompt()
    
    save(db_path, messages)
    return None

def save(db_path, messages):
    for message in messages:
        emb = embeddings.generate(message["content"])
        insert_record(db_path, message, emb)
