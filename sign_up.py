import streamlit as st


st.set_page_config(
    page_title="تسجيل حساب جديد",
    page_icon="📝",
    layout="centered"
)

st.markdown("""
    <style>
        .main {
            max-width: 400px;
            padding: 2rem;
            margin: auto;
        }
        .stButton>button {
            width: 100%;
            border-radius: 20px;
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        .stTextInput>div>div>input {
            border-radius: 20px;
            padding: 10px;
        }
        h1 {
            text-align: center;
            color: #2c3e50;
        }
    </style>
""", unsafe_allow_html=True)

if 'users' not in st.session_state:
    st.session_state.users = {
        'admin': {
            'password': 'admin123',
            'email': 'admin@example.com',
            'full_name': 'Admin User'
        }
    }


st.title("إنشاء حساب جديد")

with st.form("signup_form"):
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("الاسم الأول", key="first_name")
    with col2:
        last_name = st.text_input("اللقب", key="last_name")
    
    username = st.text_input("اسم المستخدم", help="يجب أن يكون فريداً")
    email = st.text_input("البريد الإلكتروني", type="default")
    
    col3, col4 = st.columns(2)
    with col3:
        password = st.text_input("كلمة المرور", type="password", key="password")
    with col4:
        confirm_password = st.text_input("تأكيد كلمة المرور", type="password", key="confirm_password")
    
    terms = st.checkbox("أوافق على الشروط والأحكام")
    
    submit_button = st.form_submit_button("إنشاء الحساب")


if submit_button:
    if not all([first_name, last_name, username, email, password, confirm_password]):
        st.error("الرجاء ملء جميع الحقول المطلوبة")
    elif password != confirm_password:
        st.error("كلمتا المرور غير متطابقتين")
    elif not terms:
        st.error("يجب الموافقة على الشروط والأحكام")
    elif username in st.session_state.users:
        st.error("اسم المستخدم مستخدم مسبقاً")
    else:
   
        st.session_state.users[username] = {
            'password': password,
            'email': email,
            'full_name': f"{first_name} {last_name}",
            'first_name': first_name,
            'last_name': last_name
        }
        
        st.success("✅ تم إنشاء الحساب بنجاح!")
        st.balloons()
        
      
        st.info("""
        **تم التسجيل بنجاح!**
        - يمكنك الآن تسجيل الدخول باستخدام بيانات الاعتماد الخاصة بك
        - تحقق من بريدك الإلكتروني للتحقق من الحساب
        """)

# Add a login link
st.markdown("""
<div style="text-align: center; margin-top: 20px;">
    لديك حساب بالفعل؟ <a href="#" target="_self">تسجيل الدخول</a>
</div>
""", unsafe_allow_html=True)


