import streamlit as st
import requests


st.title("📄 PDF Chat Assistant")


question = st.text_input(
    "Ask your question:"
)


if st.button("Send"):

    response = requests.post(
        "http://127.0.0.1:8000/ask",
        json={
            "question": question
        }
    )

    result = response.json()


    st.subheader("Answer")

    st.write(
        result["answer"]
    )


    st.subheader("📚 Sources")

    for source in result.get("sources", []):

        page = source.get("page")

        file = source.get("source")

        st.write(
            f"📄 {file} - Page {page + 1}"
        )