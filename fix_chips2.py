with open('streamlit_app.py', 'r') as f:
    content = f.read()

old = """# Show hint chips only when no messages
if not st.session_state.messages:
    st.markdown("<div style='text-align:center;font-size:12px;color:#9aaa9a;margin:24px 0 10px;text-transform:uppercase;letter-spacing:0.5px;'>Try asking</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    suggestions = [
        "What's Sardine's ML stack?",
        "Who leads data at Plaid?",
        "Any new AI teams at Guidewire?",
        "Marqeta tech stack",
        "Majesco AI initiatives",
        "Plaid recent funding"
    ]
    for i, suggestion in enumerate(suggestions):
        with cols[i % 3]:
            if st.button(suggestion, use_container_width=True, key=f"chip_{i}"):
                st.session_state.messages.append({"role": "user", "content": suggestion})
                st.rerun()"""

new = """# Show hint chips only when no messages
if not st.session_state.messages:
    st.markdown(\"\"\"
    <div style='text-align:center;margin:24px 0 8px;'>
        <div style='font-size:12px;color:#9aaa9a;margin-bottom:10px;text-transform:uppercase;letter-spacing:0.5px;'>Try asking</div>
        <span class='chip'>What's Sardine's ML stack?</span>
        <span class='chip'>Who leads data at Plaid?</span>
        <span class='chip'>Any new AI teams at Guidewire?</span>
        <span class='chip'>Marqeta tech stack</span>
        <span class='chip'>Majesco AI initiatives</span>
    </div>
    <div style='text-align:center;margin:16px 0;'>
        <div style='font-size:12px;color:#9aaa9a;margin-bottom:10px;text-transform:uppercase;letter-spacing:0.5px;'>What I can research</div>
        <span class='chip'>AI/ML stack</span>
        <span class='chip'>Key people + LinkedIn</span>
        <span class='chip'>Funding & news</span>
        <span class='chip'>Hiring signals</span>
        <span class='chip'>Blogs & talks</span>
    </div>
    \"\"\", unsafe_allow_html=True)"""

content = content.replace(old, new)

with open('streamlit_app.py', 'w') as f:
    f.write(content)

print("Done")
