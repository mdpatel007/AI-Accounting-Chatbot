import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.title("🤖 Hellobooks AI Accounting Chatbot")

if "file_text" not in st.session_state:
    st.session_state["file_text"] = ""

# File Upload Section
uploaded_file = st.file_uploader("Upload a TXT or Markdown file", type=["txt", "md"])

if uploaded_file:
    st.write(f"✅ File uploaded: {uploaded_file.name}")

    # Send proper tuple 
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    res = requests.post(f"{API_URL}/process_file", files=files)

    if res.status_code == 200:
        data = res.json()
        st.success(data.get("message", "✅ File processed"))

        if "text_preview" in data:
            st.text_area("Extracted Content", data["text_preview"], height=200)
    else:
        st.error("File processing failed")

# Chat Interface
user_id = st.sidebar.text_input("Enter your User ID:", value="user123")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Hit backend query_vector
    response = requests.post(f"{API_URL}/query_vector", json={
        "user_id": user_id,
        "query": prompt,
        "collection_name": "documents",
        "top_k": 3,
        "chat_history": st.session_state.messages
    })

    if response.status_code == 200:
        data = response.json()
        bot_reply = data["answer"]

        with st.chat_message("assistant"):
            st.markdown(bot_reply)

        if not data.get("irrelevant_to_pdf", False):
            retrieved = data.get("retrieved_chunks", [])
            if retrieved:
                with st.expander("Retrieved Context"):
                    for i, c in enumerate(retrieved, 1):
                        st.write(f"**Chunk {i} (score: {c['score']:.2f})**")
                        st.write(c["text_snippet"])
                        st.write("---")

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    else:
        st.error("Backend error check FastAPI server.")
