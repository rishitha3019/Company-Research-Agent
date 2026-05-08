import os
import streamlit as st
from anthropic import Anthropic

st.set_page_config(
    page_title="Company Research Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
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
section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e8f0e8 !important;
    min-width: 220px !important;
    max-width: 280px !important;
}
section[data-testid="stSidebar"] * { color: #1a1a1a !important; }
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
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.markdown("""
    <div style='padding:8px 0 16px;'>
        <div style='display:flex;align-items:center;gap:8px;margin-bottom:4px;'>
            <div style='width:10px;height:10px;border-radius:50%;background:#1D9E75;'></div>
            <span style='font-size:15px;font-weight:600;color:#1a1a1a;'>Research Agent</span>
        </div>
        <div style='font-size:12px;color:#6b7c6b;'>Powered by Claude + Web Search</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("+ New Research", use_container_width=True):
        if st.session_state.messages:
            first_msg = st.session_state.messages[0]["content"]
            company = first_msg[:40] + "..." if len(first_msg) > 40 else first_msg
            st.session_state.history = [company] + st.session_state.history[:4]
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("<div style='font-size:11px;color:#9aaa9a;letter-spacing:0.5px;text-transform:uppercase;margin-bottom:8px;'>What I can research</div>", unsafe_allow_html=True)
    for item in ["AI/ML stack & initiatives", "Tech stack & tools", "Key people + LinkedIn", "Recent news & funding", "Hiring signals", "Blogs, talks & content"]:
        st.markdown(f"<div style='font-size:12px;color:#4a6a4a;padding:3px 0;'>→ {item}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='font-size:11px;color:#9aaa9a;margin-bottom:6px;'>Try asking:</div>", unsafe_allow_html=True)
    for q in ["What's Sardine's ML stack?", "Who leads data at Plaid?", "Any new AI teams at Guidewire?"]:
        st.markdown(f"<div style='font-size:12px;color:#6b7c6b;font-style:italic;padding:2px 0;'>\"{q}\"</div>", unsafe_allow_html=True)

    if st.session_state.history:
        st.markdown("---")
        st.markdown("<div style='font-size:11px;color:#9aaa9a;letter-spacing:0.5px;text-transform:uppercase;margin-bottom:8px;'>Recent</div>", unsafe_allow_html=True)
        for item in st.session_state.history:
            st.markdown(f"<div style='font-size:12px;color:#4a6a4a;padding:4px 0;border-bottom:1px solid #f0f0f0;'>🔍 {item}</div>", unsafe_allow_html=True)

st.title("Company Research Agent")
st.caption("Ask anything about a company — tech stack, team, AI initiatives, LinkedIn profiles, recent news.")

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

# Force sidebar open
st.markdown("""
<script>
window.addEventListener('load', function() {
    setTimeout(function() {
        var btn = window.parent.document.querySelector('[data-testid="collapsedControl"]');
        if (btn) btn.click();
    }, 500);
});
</script>
""", unsafe_allow_html=True)
