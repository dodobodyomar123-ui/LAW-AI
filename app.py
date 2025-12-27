import streamlit as st
import google.generativeai as genai
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

st.set_page_config(
    page_title="المساعد القانوني المصري",
    page_icon="⚖️"
)

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader(
    "📄 ارفع ملف PDF للقانون",
    type=["pdf"]
)

if uploaded_file:
    with st.spinner("جاري معالجة الملف..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        loader = PyPDFLoader(tmp_path)
        pages = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = text_splitter.split_documents(pages)

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        st.session_state.vectorstore = FAISS.from_documents(chunks, embeddings)

    st.success("✔️ تم تحميل ومعالجة الملف بنجاح!")



st.title("⚖️ المساعد القانوني المصري")
st.info("💡 هذا المساعد يقدم معلومات عامة وليس بديلاً عن محامٍ")

with st.sidebar:
    st.markdown("### 📋 معلومات")
    st.markdown("""
    يساعدك في:
    - فهم القوانين المصرية
    - الإجراءات القانونية
    - الأسئلة العامة
    """)
    
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.chat_history = []
        st.rerun()

selected_topic = None
if len(st.session_state.chat_history) == 0:
    selected_topic = st.pills(
        "مواضيع شائعة:",
        [
            "قانون العمل",
            "قانون الأحوال الشخصية",
            "القانون المدني",
            "القانون الجنائي",
            "قانون الإيجارات",
            "قانون التجارة"
        ],
        selection_mode="single"
    )

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_question = st.chat_input("اكتب سؤالك القانوني هنا...")

if selected_topic:
    user_question = f"أخبرني عن {selected_topic} في القانون المصري"

if user_question:
    st.session_state.chat_history.append(
        {"role": "user", "content": user_question} 
    )

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("جاري البحث..."):
            answer = get_ai_response(user_question)
            st.markdown(answer)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": answer}
    )

    st.rerun()