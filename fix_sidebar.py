with open('streamlit_app.py', 'r') as f:
    content = f.read()

css = """
[data-testid="collapsedControl"] {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
}
"""

content = content.replace('</style>', css + '</style>')

with open('streamlit_app.py', 'w') as f:
    f.write(content)

print("Done")
