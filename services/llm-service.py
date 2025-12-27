import streamlit as st
import google.generativeai as genai





def get_ai_response(user_question):
    try:
        GOOGLE_API_KEY = "AIzaSyAcpxzbnfE-uCmKZFl77sbWR9WnTAdTeno"

        genai.configure(api_key=GOOGLE_API_KEY)

        model = genai.GenerativeModel("gemini-2.5-flash")

        context = ""
        found_info = False

        if st.session_state.vectorstore:
            results = st.session_state.vectorstore.similarity_search(
                user_question,
                k=3
            )
            
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
