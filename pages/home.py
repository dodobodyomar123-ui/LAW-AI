import streamlit as st

def render():
    st.set_page_config(
        page_title="المساعد القانوني المصري",
        page_icon="⚖️",
    )

    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.title("⚖️ المساعد القانوني المصري")
    st.info("💡 هذا المساعد يقدم معلومات عامة وليس بديلاً عن محامٍ")

    st.markdown("### ابدأ")
    st.write("استخدم صفحة المحادثة لرفع ملف PDF وطرح أسئلتك.")

    if st.button("الانتقال إلى المحادثة"):
        st.switch_page("pages/chat.py")


if __name__ == "__main__":
    render()
