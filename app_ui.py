
import streamlit as st
import requests

st.set_page_config(
    page_title="GuardRail-RAG",
    page_icon="🔐",
    layout="centered",
)

API_URL = "http://127.0.0.1:8000"

st.title("🔐 GuardRail-RAG")
st.caption("Permission-aware, multi-tenant document assistant")

# Login
st.subheader("Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    try:
        response = requests.post(
            f"{API_URL}/login",
            json={"email": email, "password": password},
            timeout=15,
        )

        if response.status_code == 200:
            st.session_state["token"] = response.json()["access_token"]
            st.session_state["email"] = email
            st.success("Login successful!")
        else:
            st.error(
                f"Login failed ({response.status_code}): "
                f"{response.text}"
            )

    except requests.RequestException as e:
        st.error(f"Login request failed: {e}")

# Question and answer
st.divider()
st.subheader("Ask your documents")

if st.session_state.get("token"):
    question = st.text_area(
        "Enter your question",
        placeholder="Ask about your authorized documents...",
    )

    if st.button("Ask", type="primary"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"question": question},
                    headers={
                        "Authorization":
                            f"Bearer {st.session_state['token']}"
                    },
                    timeout=90,
                )

                if response.status_code == 200:
                    result = response.json()
                    st.markdown("### Answer")
                    st.write(result["answer"])
                elif response.status_code == 401:
                    st.session_state.pop("token", None)
                    st.error("Session expired. Please log in again.")
                else:
                    st.error(
                        f"Ask request failed ({response.status_code}): "
                        f"{response.text}"
                    )

            except requests.RequestException as e:
                st.error(f"Ask request failed: {e}")
else:
    st.info("Please log in above to ask questions.")
