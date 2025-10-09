import context
import groq_API

def engine():
    question = input("Ask Your Question : \n")
    
    while question.lower() != "exit":
        ctx = context.manager(question)
    
        prompt = f"""### Context: \n{ctx}\n### Question: {question}\n### Answer:"""
        print("\n\n-------------------------context-------------------------\n\n", ctx)
    
        print("\n\n-------------------------response-------------------------\n\n")
        try:
            completion = groq_API.ask(prompt)
            for chunk in completion:
                print(chunk.choices[0].delta.content or "", end="")
        except Exception as e:
            print(f"Error Connecting to API: {e}")
            
        print("\n\n-------------------------prompt-------------------------\n\n")
        question = input()
    
if __name__ == "__main__":
    engine()
