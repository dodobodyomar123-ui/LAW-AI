import streamlit as st

if 'users' not in st.session_state:
    st.session_state.users = {
        'admin': {
            'password': 'admin123',  
            'email': 'admin@example.com',
            'full_name': 'Admin User'
        }
    }

def login_form():
    with st.form("login_form"):
        st.subheader("تسجيل الدخول")
        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        submit = st.form_submit_button("دخول")
        
        if submit:
            if username in st.session_state.users and \
               st.session_state.users[username]['password'] == password:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.rerun()
            else:
                st.error("اسم المستخدم أو كلمة المرور غير صحيحة")
        return False

def signup_form():
    with st.form("signup_form"):
        st.subheader("إنشاء حساب جديد")
        username = st.text_input("اسم المستخدم")
        email = st.text_input("البريد الإلكتروني")
        full_name = st.text_input("الاسم الكامل")
        password = st.text_input("كلمة المرور", type="password")
        confirm_password = st.text_input("تأكيد كلمة المرور", type="password")
        submit = st.form_submit_button("إنشاء حساب")
        
        if submit:
            if password != confirm_password:
                st.error("كلمتا المرور غير متطابقتين")
            elif username in st.session_state.users:
                st.error("اسم المستخدم مستخدم مسبقاً")
            else:
                st.session_state.users[username] = {
                    'password': password,  
                    'email': email,
                    'full_name': full_name
                }
                st.success("تم إنشاء الحساب بنجاح! يرجى تسجيل الدخول.")
                return True
        return False

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


if not st.session_state.logged_in:
    st.title("نظام المساعدة القانونية")
    tab1, tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب جديد"])
    
    with tab1:
        if login_form():
            st.rerun()
    
    with tab2:
        if signup_form():
            st.rerun()
    st.stop()


st.sidebar.title(f"مرحباً، {st.session_state.username}")
if st.sidebar.button("تسجيل الخروج"):
    st.session_state.logged_in = False
    st.session_state.pop('username', None)
    st.rerun()


st.title("مساعد القانون المصري")
st.write("مرحباً بك في نظام المساعدة القانونية")

