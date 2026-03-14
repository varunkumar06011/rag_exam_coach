import streamlit as st
from src.rag_pipeline import build_vectorstore, retrieve_chunks
from src.question_generator import generate_questions
from src.topic_tracker import update_tracker, get_weak_topics, reset_tracker
from src.utils import extract_text_from_pdf
import os

st.set_page_config(
    page_title="Finish Task – Smart Study Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS Redesign ──
st.markdown("""
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

    /* Global Body styling */
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif !important;
        background-color: #F8FAFC !important; /* Very soft pastel blue/grey background */
    }
    
    /* Main Content Area */
    .stApp {
        background-color: #F8FAFC;
    }

    /* Streamlit Containers -> Transform into 'Cards' */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); /* Soft drop shadow */
        border: 1px solid #E2E8F0;
        margin-bottom: 24px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"]:hover {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08); /* Lift effect on hover */
    }

    /* Scrolling Motivational Banner */
    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        background-color: #E6F0FA; /* Soft light blue */
        padding: 12px 0;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
        border: 1px solid #D6E4F0;
    }
    .ticker {
        display: inline-block;
        white-space: nowrap;
        animation: ticker 25s linear infinite;
        font-weight: 700;
        color: #2B6CB0; /* Deep blue font */
        font-size: 1.1rem;
    }
    @keyframes ticker {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    .ticker span {
        margin: 0 50px;
    }

    /* Upload Box Tweaks */
    section[data-testid="stFileUploadDropzone"] {
        border-radius: 12px;
        border: 2px dashed #90CDF4 !important;
        background-color: #F7FAFC;
        transition: all 0.2s;
    }
    section[data-testid="stFileUploadDropzone"]:hover {
        background-color: #EDF2F7;
        border-color: #4299E1 !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4299E1 0%, #3182CE 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px 24px;
        font-weight: 700;
        transition: all 0.2s ease;
        box-shadow: 0 4px 6px rgba(49, 130, 206, 0.2);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 10px rgba(49, 130, 206, 0.3);
        background: linear-gradient(135deg, #3182CE 0%, #2B6CB0 100%);
    }

    /* Sidebar Clean Up */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
        padding-top: 2rem;
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        color: #2D3748 !important;
    }
    h1 {
        font-weight: 800 !important;
        letter-spacing: -0.02em;
    }
    </style>
""", unsafe_allow_html=True)

# Try to get API key from Streamlit secrets (Cloud) or Environment Variables (Local/.env)
try:
    # Check if the secrets file exists first so Streamlit doesn't auto-warn
    if os.path.exists(".streamlit/secrets.toml"):
        # The key might be under a [secret] block or at the root level depending on the TOML format
        if "secret" in st.secrets:
            GROQ_API_KEY = st.secrets["secret"].get("GROQ_API_KEY")
        else:
            GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
    else:
        GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
except Exception:
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# ── Session State Init ──
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "tracker" not in st.session_state:
    st.session_state.tracker = {}
if "history" not in st.session_state:
    st.session_state.history = []
if "doc_name" not in st.session_state:
    st.session_state.doc_name = None

# ── Motivational Scrolling Banner ──
st.markdown("""
<div class="ticker-wrap">
    <div class="ticker">
        <span>🎓 Finish Task – Smart Study Assistant</span>
        <span>🚀 Stay consistent. Small progress daily leads to big success.</span>
        <span>💡 Discipline beats motivation.</span>
        <span>🌟 Your future self will thank you.</span>
        <span>🎯 Focus. Learn. Improve.</span>
        <span>📚 Every question solved is a step closer to mastery.</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Header ──
st.title("Finish Task – Smart Study Assistant")
st.markdown("##### Transform your syllabus into practice exams instantly.")
st.write("") # Spacer

# ── Sidebar ──
with st.sidebar:
    st.title("⚙️ Study Preferences")
    st.divider()
    
    language = st.selectbox("Output Language", ["English", "Telugu"])
    difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
    num_questions = st.slider("Number of Questions", min_value=3, max_value=15, value=5)
    
    st.divider()
    
    st.title("📊 Weak Topic Tracker")
    weak = get_weak_topics(st.session_state.tracker)
    if weak:
        for topic, count in weak.items():
            st.markdown(f"🔹 **{topic}** (Revisited: {count}x)")
    else:
        st.info("Start studying to track your weak areas!")
        
    if st.button("🔄 Clean Slate"):
        reset_tracker()
        st.session_state.tracker = {}
        st.success("Tracker reset!")

# ── Main UI Cards ──
col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    # Card 1: Study Material Upload
    with st.container():
        st.subheader("📁 Upload Study Material")
        uploaded_file = st.file_uploader(
            "Upload your Syllabus or textbook chapter (PDF or TXT)",
            type=["pdf", "txt"],
            help="Limit 200MB per file. High-quality text PDFs work best."
        )

        if uploaded_file and GROQ_API_KEY:
            if st.session_state.doc_name != uploaded_file.name:
                with st.spinner("Processing document..."):
                    if uploaded_file.type == "application/pdf":
                        text = extract_text_from_pdf(uploaded_file)
                    else:
                        text = uploaded_file.read().decode("utf-8")

                    st.session_state.vectorstore = build_vectorstore(text)
                    st.session_state.doc_name = uploaded_file.name
                    st.success(f"✅ Document '{uploaded_file.name}' loaded successfully! You are ready to study.")

        elif uploaded_file and not GROQ_API_KEY:
            st.error("⚠️ Server Configuration Error: `GROQ_API_KEY` is not set in the backend environment.")

with col2:
    # Card 2: Topic Focus
    with st.container():
        st.subheader("🎯 Refine Focus (Optional)")
        topic_input = st.text_input(
            "Enter a specific topic to study right now",
            placeholder="e.g. Neural Networks, Recursion, Laws of Motion"
        )
        st.caption("Leave blank to generate questions from the entire document overview.")

st.write("") # Spacer

# ── Card 3: Question Generator ──
with st.container():
    if st.session_state.vectorstore and GROQ_API_KEY:
        st.subheader("🚀 Let's Go!")
        if st.button("Generate Exam Questions", use_container_width=True):
            with st.spinner("Analyzing material and generating questions..."):
                query = topic_input if topic_input else "main concepts and important topics"
                chunks = retrieve_chunks(st.session_state.vectorstore, query)

                questions = generate_questions(
                    chunks=chunks,
                    difficulty=difficulty,
                    language=language,
                    num_questions=num_questions,
                    api_key=GROQ_API_KEY,
                    topic=topic_input
                )

                # Track topic
                if topic_input:
                    st.session_state.tracker = update_tracker(
                        st.session_state.tracker, topic_input
                    )

                # Store in history
                st.session_state.history.append({
                    "topic": topic_input or "Overview",
                    "difficulty": difficulty,
                    "language": language,
                    "questions": questions
                })

# ── Card 4: Display Output ──
if st.session_state.history:
    st.write("---")
    with st.container():
        latest = st.session_state.history[-1]
        st.subheader(f"📝 Practice Questions — Focus: {latest['topic']}")
        st.caption(f"Difficulty: {latest['difficulty']} | Language: {latest['language']}")
        st.write("")
        st.markdown(latest["questions"])
        
        # History expander
        if len(st.session_state.history) > 1:
            st.write("---")
            with st.expander("📚 View Previous Sessions"):
                for i, session in enumerate(reversed(st.session_state.history[:-1]), 1):
                    st.markdown(f"**Session {len(st.session_state.history) - i}** — Topic: {session['topic']} | {session['difficulty']} | {session['language']}")
                    st.markdown(session["questions"])
                    st.divider()

elif not st.session_state.vectorstore:
    st.info("👆 Upload a document above to unlock your smart study session.")
