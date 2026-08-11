from llm import ask_llm, LLMError


def main():
    print("AI Assistant")
    print("برای خروج exit بنویس.\n")

    while True:

        user_message = input("You: ")

        if user_message.lower() == "exit":
            print("Bye!")
            break

        try:
            answer = ask_llm(user_message)

            print(f"\nAssistant: {answer}\n")

        except ValueError as error:
            print(f"\nInput Error: {error}\n")

        except LLMError as error:
            print(f"\nLLM Error: {error}\n")


if __name__ == "__main__":
    main()