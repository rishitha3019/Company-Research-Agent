import re

with open('streamlit_app.py', 'r') as f:
    content = f.read()

avatar_css = """
[data-testid="stChatMessageAvatarUser"] {
    background-color: #1D9E75 !important;
    color: white !important;
}
[data-testid="stChatMessageAvatarAssistant"] {
    background-color: #EAF3DE !important;
    color: #3B6D11 !important;
}
[data-testid="stChatMessageAvatarUser"] img,
[data-testid="stChatMessageAvatarAssistant"] img {
    display: none !important;
}
"""

content = content.replace('</style>', avatar_css + '</style>')

with open('streamlit_app.py', 'w') as f:
    f.write(content)

print("Done")
