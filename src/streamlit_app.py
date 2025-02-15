import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/nl2sql/"

st.title("🗄️ NL2SQL Chatbot")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# User input field
user_input = st.text_input("🔍 Ask your database:")

if st.button("Generate SQL"):
    if user_input:
        # Add user input to session state memory
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # Send request to FastAPI
        response = requests.post(API_URL, json={"question": user_input, "messages": st.session_state["messages"]})

        if response.status_code == 200:
            sql_query = response.json()["sql_query"]

            # Add assistant response to session state memory
            st.session_state["messages"].append({"role": "assistant", "content": sql_query})

            # Display SQL query result
            st.code(sql_query)
        else:
            st.error("⚠️ Error fetching SQL query!")

# Display chat history
st.subheader("💬 Chat History")
for msg in st.session_state["messages"]:
    role = "👤 User" if msg["role"] == "user" else "🤖 Assistant"
    st.write(f"**{role}:** {msg['content']}")

# Button to clear chat history
if st.button("🗑️ Clear Chat History"):
    st.session_state["messages"] = []
    st.experimental_rerun()
