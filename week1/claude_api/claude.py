import streamlit as st
from openai import OpenAI

st.title("چت با Claude")

client = OpenAI(
    api_key="aa-6M4Rt1LNpJHylgdRBZxkQ3MDcWtJbOJLdBRAWaWpyIQVoQrL",
    base_url="https://api.avalai.ir/v1",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("پیامت رو بنویس...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    response = client.chat.completions.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        messages=[{"role": "system", "content": "تو یک دستیار فارسی‌زبان هستی."}] + st.session_state.messages
    )
    reply = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)