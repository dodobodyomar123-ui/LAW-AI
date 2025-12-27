import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def build_vectorstore_from_uploaded_pdf(
    uploaded_file,
    *,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
):
    if uploaded_file is None:
        return None

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    loader = PyPDFLoader(tmp_path)
    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = text_splitter.split_documents(pages)

    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    return FAISS.from_documents(chunks, embeddings)
