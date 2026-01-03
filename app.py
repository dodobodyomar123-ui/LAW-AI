import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables (like API keys)
load_dotenv()

st.set_page_config(
    page_title="المساعد القانوني المصري", page_icon="⚖️", layout="centered"
)

# Custom Styling
st.markdown(
    """
    <style>
        .main-title {
            text-align: center;
            color: #2c3e50;
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 2rem;
            font-size: 1.2rem;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Main Interface
st.markdown(
    "<h1 class='main-title'>⚖️ المساعد القانوني المصري</h1>", unsafe_allow_html=True
)
st.markdown(
    "<p class='subtitle'>نظام ذكي لمساعدتك في فهم الوثائق القانونية المصرية</p>",
    unsafe_allow_html=True,
)

# Introduction
st.info(
    "💡 هذا المساعد يقدم معلومات عامة للمساعدة، ولا يعد بديلاً عن الاستشارة القانونية من محامٍ مختص."
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📄 تلخيص المستندات")
    st.write("ارفع ملفات PDF (قوانين، عقود، أحكام) واحصل على ملخص فوري.")

with col2:
    st.markdown("### 💬 اسأل المساعد")
    st.write("اطرح أي سؤال حول محتوى مستنداتك وسيقوم النظام بالإجابة.")

st.divider()

# Call to Action
st.write("### للبدء، يرجى تسجيل الدخول أو إنشاء حساب جديد")

if st.button("تسجيل الدخول / إنشاء حساب", type="primary"):
    st.switch_page("pages/auth.py")
