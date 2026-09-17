from chains.summarizer_chain import summarizer_chain
from chains.report_chain import report_chain

from tools.rag_tool import rag_search


def research_assistant(question: str):

    rag_result = rag_search.invoke(
        question
    )


    summary = summarizer_chain.invoke(
        {
            "paper": rag_result["answer"]
        }
    )


    report = report_chain.invoke(
        {
            "analysis": summary,
            "sources": str(
                rag_result["sources"]
            ),
        }
    )


    return report



if __name__ == "__main__":

    question = (
        "What are the major development "
        "trends of intelligent technologies?"
    )


    result = research_assistant(
        question
    )


    print(result)