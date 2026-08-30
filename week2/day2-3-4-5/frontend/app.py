import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


st.title("📄 PDF Chat Assistant")


# -------------------------
# Upload PDF
# -------------------------

st.subheader("📤 Upload PDF")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)


if uploaded_file is not None:

    if st.button("Upload"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                "application/pdf"
            )
        }

        try:

            response = requests.post(
                f"{API_URL}/upload-pdf",
                files=files
            )

            result = response.json()


            if response.status_code == 200:

                st.success(
                    "PDF processed successfully ✅"
                )

                st.write(result)

            else:

                st.error(result)


        except Exception as e:

            st.error(
                f"Upload failed: {e}"
            )


# -------------------------
# Ask Question
# -------------------------

st.divider()

st.subheader("💬 Ask your question")


question = st.text_input(
    "Question:"
)


if st.button("Send"):

    try:

        response = requests.post(
            f"{API_URL}/ask",
            json={
                "question": question
            }
        )


        result = response.json()


        if response.status_code == 200:

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


        else:

            st.error(result)


    except Exception as e:

        st.error(
            f"Request failed: {e}"
        )