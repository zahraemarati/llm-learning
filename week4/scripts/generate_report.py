from pathlib import Path

from agents.research_assistant import research_assistant


OUTPUT_FILE = Path(
    "report/research_report.md"
)


def generate_report():

    question = (
        "Research the major development "
        "trends of intelligent technologies."
    )


    report = research_assistant(
        question
    )


    OUTPUT_FILE.parent.mkdir(
        exist_ok=True
    )


    OUTPUT_FILE.write_text(
        report,
        encoding="utf-8"
    )


    return report



if __name__ == "__main__":

    result = generate_report()

    print(
        "Report generated:"
    )

    print(
        OUTPUT_FILE
    )