import streamlit as st
from utils.config import PAGE_TITLE, PAGE_ICON, LAYOUT
from utils.session_manager import initialize_session_state, is_logged_in
from components.login_view import render_login_view
from components.wallet_header import render_wallet_header
from components.send_tab import render_send_tab
from components.history_tab import render_history_tab

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=LAYOUT)

st.markdown("""
<style>
@keyframes fadeOut {
    0% { opacity: 1; transform: translateY(0); }
    90% { opacity: 0; transform: translateY(-10px); }
    100% { opacity: 0; display: none; }
}
div[data-testid="stNotification"] {
    animation: fadeOut 0.5s ease-in-out 4.5s forwards;
}
</style>
<script>
setTimeout(() => {
    document.querySelectorAll('[data-testid="stNotification"]').forEach(el => {
        el.style.transition = 'opacity 0.5s, transform 0.5s';
        el.style.opacity = '0';
        el.style.transform = 'translateY(-10px)';
        setTimeout(() => el.remove(), 500);
    });
}, 5000);
</script>
""", unsafe_allow_html=True)

initialize_session_state()
st.title(f"{PAGE_ICON} {PAGE_TITLE}")

if not is_logged_in():
    render_login_view()
else:
    render_wallet_header()
    tab1, tab2 = st.tabs(["📤 Send", "📜 History"])
    with tab1:
        render_send_tab()
    with tab2:
        render_history_tab()

st.markdown("---")
st.markdown(f"<div style='text-align: center; color: gray;'>{PAGE_TITLE} | Built with FastAPI & Streamlit</div>", unsafe_allow_html=True)
