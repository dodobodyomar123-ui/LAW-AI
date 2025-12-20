import streamlit as st
import google.generativeai as genai

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ================= Page config =================
st.set_page_config(page_title="مساعد القانون المصري", page_icon="⚖️")


# ================= Session state =================
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ================= File upload =================
uploaded_file = st.file_uploader("📄 ارفع ملف PDF للقانون", type=["pdf"])

if uploaded_file:
    with st.spinner("جاري معالجة الملف..."):
        # ✅ SAVE PDF TEMPORARILY (FIX)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        # ✅ LOAD PDF CORRECTLY
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

    st.success("✔️ تم تحميل ومعالجة ملف PDF بنجاح!")


# ================= AI RESPONSE =================
def get_ai_response(user_question):
    try:
        GOOGLE_API_KEY = "AIzaSyAcpxzbnfE-uCmKZFl77sbWR9WnTAdTeno"
        genai.configure(api_key=GOOGLE_API_KEY)

        model = genai.GenerativeModel("gemini-2.5-flash")

        context = ""
        found_info = False

        if st.session_state.vectorstore:
            results = st.session_state.vectorstore.similarity_search(user_question, k=3)
            for doc in results:
                if doc.page_content.strip():
                    found_info = True
                    context += doc.page_content + "\n"

        if found_info:
            instructions = f"""
أنت مساعد قانوني متخصص في القانون المصري.

استخدم فقط المعلومات التالية من ملف PDF:
{context}

قواعد:
- أجب باللغة العربية
- اذكر أرقام المواد إن أمكن
- هذه ليست استشارة قانونية رسمية

سؤال المستخدم:
{user_question}
"""
        else:
            instructions = f"""
لم يتم العثور على إجابة داخل ملف PDF.

- أجب من معرفتك العامة
- نبه المستخدم أن الإجابة ليست من الملف

سؤال المستخدم:
{user_question}
"""

        response = model.generate_content(instructions)
        return response.text

    except Exception as e:
        return f"حدث خطأ: {str(e)}"


# ================= UI =================
st.title("⚖️ مساعد القانون المصري")
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


# ================= Topics =================
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


# ================= Chat =================
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
