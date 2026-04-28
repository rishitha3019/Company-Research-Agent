with open('streamlit_app.py', 'r') as f:
    content = f.read()

old = """    if st.button("+ New Research", use_container_width=True):
        st.session_state.messages = []
        st.rerun()"""

new = """    if st.button("+ New Research", use_container_width=True):
        if st.session_state.messages:
            if "history" not in st.session_state:
                st.session_state.history = []
            # Extract company name from first user message
            first_msg = st.session_state.messages[0]["content"]
            company = first_msg[:40] + "..." if len(first_msg) > 40 else first_msg
            st.session_state.history = [company] + st.session_state.history[:4]
        st.session_state.messages = []
        st.rerun()

    if "history" not in st.session_state:
        st.session_state.history = []

    if st.session_state.history:
        st.markdown("---")
        st.markdown("<div style='font-size:11px;color:#9aaa9a;letter-spacing:0.5px;text-transform:uppercase;margin-bottom:8px;'>Recent</div>", unsafe_allow_html=True)
        for item in st.session_state.history:
            st.markdown(f"<div style='font-size:12px;color:#4a6a4a;padding:4px 0;border-bottom:1px solid #f0f0f0;'>🔍 {item}</div>", unsafe_allow_html=True)"""

content = content.replace(old, new)

with open('streamlit_app.py', 'w') as f:
    f.write(content)

print("Done")
