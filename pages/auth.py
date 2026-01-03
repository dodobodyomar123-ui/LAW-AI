import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.auth_service import login_user, register_user, logout_user

st.set_page_config(page_title="تسجيل الدخول", page_icon="🔐")

# --- Check Login Status ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.success(f"مرحباً بك، {st.session_state.username}!")
    if st.button("الذهاب إلى المحادثة"):
        st.switch_page("pages/chat.py")
    if st.button("تسجيل الخروج"):
        logout_user()
    st.stop()

# --- UI ---
st.title("🔐 بوابة الدخول")

tab1, tab2 = st.tabs(["تسجيل الدخول", "حساب جديد"])

with tab1:  # Login
    st.subheader("تسجيل الدخول")
    with st.form("login_form"):
        email = st.text_input("البريد الإلكتروني")
        password = st.text_input("كلمة المرور", type="password")
        if st.form_submit_button("دخول"):
            if login_user(email, password):
                st.success("تم الدخول بنجاح!")
                st.switch_page("pages/chat.py")
            else:
                st.error("بيانات الدخول غير صحيحة.")

with tab2:  # Signup
    st.subheader("إنشاء حساب جديد")
    with st.form("signup_form"):
        new_email = st.text_input("اختر اسم مستخدم")
        new_pass = st.text_input("كلمة المرور", type="password")
        email = st.text_input("البريد الإلكتروني")
        if st.form_submit_button("إنشاء حساب"):
            success, msg = register_user(new_email, new_pass, email)
            if success:
                st.success(msg)
            else:
                st.error(msg)
