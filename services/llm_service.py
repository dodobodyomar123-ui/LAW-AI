import os
import streamlit as st
import google.generativeai as genai


def get_ai_response(
    user_question: str, *, vectorstore=None, model_name: str = "gemini-2.5-flash"
) -> str:
    try:
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            return "حدث خطأ: لم يتم العثور على GOOGLE_API_KEY في متغيرات البيئة"

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)

        vs = vectorstore
        if vs is None:
            vs = st.session_state.get("vectorstore")

        context = ""
        found_info = False

        if vs:
            results = vs.similarity_search(user_question, k=3)
            for doc in results:
                if getattr(doc, "page_content", "").strip():
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
        return getattr(response, "text", "") or ""

    except Exception as e:
        return f"حدث خطأ: {str(e)}"
