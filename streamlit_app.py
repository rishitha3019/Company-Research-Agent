import os
import streamlit as st
from anthropic import Anthropic

st.set_page_config(
    page_title="Company Research Agent",
    page_icon="🔍",
    layout="centered"
)

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert company intelligence analyst. When a user asks about a company, you proactively research it using web search.

For every company, always try to surface:
- What the company does, their stage, funding, and investors
- Their AI/ML initiatives and how they use data
- Their tech stack (languages, frameworks, infrastructure)
- Key people in data/engineering/product with LinkedIn profile URLs
- Recent news: funding rounds, product launches, new teams
- Relevant content: blog posts, YouTube talks, conference presentations
- Current hiring signals in data/AI/ML roles

Respond conversationally with insights and links embedded naturally."""

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.stApp { background-color: #f8faf8 !important; }
[data-testid="stChatMessage"] {
    background-color: #ffffff !important;
    border: 1px solid #e8f0e8 !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
    margin: 6px 0 !important;
}
[data-testid="stChatMessage"] p { color: #1a1a1a !important; font-size: 14px !important; line-height: 1.7 !important; }
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3 { color: #1a1a1a !important; }
[data-testid="stChatMessage"] li { color: #1a1a1a !important; font-size: 14px !important; }
[data-testid="stChatMessage"] code { background-color: #EAF3DE !important; color: #3B6D11 !important; padding: 2px 6px !important; border-radius: 4px !important; }
.stChatInput textarea { background-color: #ffffff !important; color: #1a1a1a !important; border: 1px solid #c8e6c8 !important; border-radius: 12px !important; font-size: 14px !important; }
.stButton button { background-color: #1D9E75 !important; color: white !important; border: none !important; border-radius: 8px !important; font-size: 13px !important; font-weight: 500 !important; }
.chip { display: inline-block; background: #EAF3DE; color: #3B6D11; font-size: 12px; padding: 4px 12px; border-radius: 20px; margin: 3px; cursor: pointer; }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.markdown("""
<div style='text-align:center;padding:32px 0 8px;'>
    <div style='display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:6px;'>
        <div style='width:10px;height:10px;border-radius:50%;background:#1D9E75;'></div>
        <span style='font-size:26px;font-weight:600;color:#1a1a1a;letter-spacing:-0.4px;'>Company Research Agent</span>
    </div>
    <div style='font-size:14px;color:#6b7c6b;'>Powered by Claude + Web Search</div>
</div>
""", unsafe_allow_html=True)

# Show hint chips only when no messages
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
                st.rerun()

# New research button
if st.session_state.messages:
    if st.button("+ New Research"):
        st.session_state.messages = []
        st.rerun()

# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about a company..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Researching..."):
            try:
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=4096,
                    system=SYSTEM_PROMPT,
                    tools=[{"type": "web_search_20250305", "name": "web_search"}],
                    messages=st.session_state.messages
                )
                result = ""
                for block in response.content:
                    if block.type == "text":
                        result += block.text
            except Exception as e:
                result = f"Something went wrong: {e}"
        st.markdown(result)
    st.session_state.messages.append({"role": "assistant", "content": result})
