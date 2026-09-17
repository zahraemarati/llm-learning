from agents.research_assistant import research_assistant


def main():

    print("=" * 50)
    print("AI Research Assistant")
    print("=" * 50)


    question = input(
        "\nEnter your research question:\n> "
    )


    print("\nGenerating research report...\n")


    report = research_assistant(
        question
    )


    print("\n" + "=" * 50)
    print("Research Report")
    print("=" * 50)

    print(report)



if __name__ == "__main__":
    main()