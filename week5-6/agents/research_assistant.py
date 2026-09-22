from agents.research_agent import run_agent


def main():
    user_input = input("You: ")

    answer = run_agent(user_input)

    print(f"\nAssistant: {answer}")


if __name__ == "__main__":
    main()