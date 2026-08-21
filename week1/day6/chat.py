from llm_client import chat_complete
from memory import ConversationMemory

memory = ConversationMemory()

def ask(message: str) -> str:
    memory.add_user_message(message)
    reply = chat_complete(memory.get_messages())
    memory.add_assistaثnt_message(reply)
    return reply

if __name__ == "__main__":
    print("چت شروع شد. برای خروج 'exit' بنویس.\n")
    while True:
        user_input = input("شما: ")
        if user_input.strip().lower() == "exit":
            break
        print(f"دستیار: {ask(user_input)}\n")