with open('streamlit_app.py', 'r') as f:
    content = f.read()

old = 'st.set_page_config(page_title="Company Research Agent", page_icon="🔍", layout="wide")'
new = 'st.set_page_config(page_title="Company Research Agent", page_icon="🔍", layout="wide", initial_sidebar_state="expanded")'

content = content.replace(old, new)

with open('streamlit_app.py', 'w') as f:
    f.write(content)

print("Done")
