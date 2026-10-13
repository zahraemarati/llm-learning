from agents.research_agent import clear_memory, run_agent


def main():
    clear_memory()

    print("Chat started. Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in {
            "exit",
            "quit",
        }:
            break

        if not user_input:
            continue

        answer = run_agent(
            user_input,
            verbose=True,
        )

        print(f"\nAssistant: {answer}")


if __name__ == "__main__":
    main()