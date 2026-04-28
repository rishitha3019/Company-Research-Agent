with open('streamlit_app.py', 'r') as f:
    content = f.read()

css = """
section[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
button[kind="header"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: all !important;
    position: fixed !important;
    top: 1rem !important;
    left: 1rem !important;
    z-index: 9999 !important;
    background: #1D9E75 !important;
    border-radius: 8px !important;
    padding: 4px !important;
}
"""

content = content.replace('</style>', css + '</style>')

with open('streamlit_app.py', 'w') as f:
    f.write(content)

print("Done")
