import json
import os
import streamlit as st

USERS_FILE = "data/users.json"


def _load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def _save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def login_user(username_or_email, password):
    users = _load_users()

    # 1. Try Direct Username Match
    if username_or_email in users and users[username_or_email]["password"] == password:
        st.session_state.logged_in = True
        st.session_state.username = username_or_email
        return True

    # 2. Try Email Match
    for user, data in users.items():
        if data.get("email") == username_or_email and data["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = user
            return True

    return False


def register_user(username, password, email=""):
    users = _load_users()

    if not username or not password:
        return False, "الرجاء إدخال اسم المستخدم وكلمة المرور."

    if username in users:
        return False, "اسم المستخدم هذا محجوز مسبقاً."

    users[username] = {"password": password, "email": email}
    _save_users(users)
    return True, "تم إنشاء الحساب بنجاح!"


def logout_user():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()


def check_structure():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("يجب عليك تسجيل الدخول أولاً.")
        st.stop()
        return False
    return True
