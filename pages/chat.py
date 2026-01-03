import streamlit as st
import os
import sys

# Add root directory to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.document_service import get_pdf_text, get_text_chunks, get_vectorstore
from services.llm_service import get_ai_response
from services.auth_service import check_structure, logout_user

st.set_page_config(page_title="المحادثة القانونية", page_icon="💬")

# --- Security Check ---
# This single line handles validation and stopping execution if needed
check_structure()

# --- Sidebar ---
with st.sidebar:
    st.write(f"مرحباً, **{st.session_state.username}**")
    if st.button("تسجيل الخروج"):
        logout_user()  # Clean logout helper

    st.divider()
    st.subheader("مستنداتك")
    pdf_docs = st.file_uploader(
        "ارفع ملفات PDF هنا", accept_multiple_files=True, type=["pdf"]
    )

    if st.button("معالجة الملفات"):
        if not pdf_docs:
            st.error("الرجاء رفع ملفات PDF أولاً.")
        else:
            with st.spinner("جاري المعالجة..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(text_chunks)
                st.session_state.vectorstore = vectorstore
                st.success("تم الانتهاء! يمكنك الآن طرح الأسئلة.")

# --- Main Chat Interface ---
st.title("💬 المحادثة القانونية")

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Predefined Topics
topics = [
    "⚖️ قانون العمل",
    "🏠 الأحوال الشخصية",
    "📜 القانون المدني",
    "🔒 قانون العقوبات",
    "🏢 عقود الإيجار",
    "💼 قانون الشركات",
]
selected_topic = st.pills(
    "اختر موضوعاً أو اسأل سؤالك الخاص:", topics, selection_mode="single"
)

# Chat Input
user_question = st.chat_input("اطرح سؤالك حول المستندات...")

# Handle Pills Selection
if selected_topic and not user_question:
    user_question = f"أريد معرفة معلومات عن {selected_topic}"

if user_question:
    st.chat_message("user").markdown(user_question)
    st.session_state.chat_history.append({"role": "user", "content": user_question})

    with st.spinner("جاري التفكير..."):
        response = get_ai_response(
            user_question, vectorstore=st.session_state.vectorstore
        )

    st.chat_message("assistant").markdown(response)
    st.session_state.chat_history.append({"role": "assistant", "content": response})
