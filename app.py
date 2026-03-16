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

# ------------------------------
# Load API Key (Backend only)
# ------------------------------

def load_api_key():
    try:
        if os.path.exists(".streamlit/secrets.toml"):
            if "secret" in st.secrets:
                return st.secrets["secret"].get("GROQ_API_KEY")
            return st.secrets.get("GROQ_API_KEY")
        return os.environ.get("GROQ_API_KEY")
    except Exception:
        return os.environ.get("GROQ_API_KEY")

GROQ_API_KEY = load_api_key()

# Fixed model (no UI selection)
MODEL_NAME = "llama-3.1-8b-instant"

# ------------------------------
# Session State
# ------------------------------

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "tracker" not in st.session_state:
    st.session_state.tracker = {}

if "history" not in st.session_state:
    st.session_state.history = []

if "doc_name" not in st.session_state:
    st.session_state.doc_name = None


# ------------------------------
# Header
# ------------------------------

st.title("🎓 Finish Task – Smart Study Assistant")
st.markdown("Transform your syllabus into practice exams instantly.")


# ------------------------------
# Sidebar
# ------------------------------

with st.sidebar:

    st.title("⚙️ Study Preferences")

    language = st.selectbox(
        "Output Language",
        ["English", "Telugu"]
    )

    difficulty = st.selectbox(
        "Difficulty Level",
        ["Easy", "Medium", "Hard"]
    )

    num_questions = st.slider(
        "Number of Questions",
        3,
        15,
        5
    )

    st.divider()

    st.subheader("📊 Weak Topic Tracker")

    weak_topics = get_weak_topics(st.session_state.tracker)

    if weak_topics:
        for topic, count in weak_topics.items():
            st.markdown(f"🔹 **{topic}** (Revisited {count} times)")
    else:
        st.info("Start studying to track weak areas.")

    if st.button("🔄 Reset Tracker"):
        reset_tracker()
        st.session_state.tracker = {}
        st.success("Tracker reset.")


# ------------------------------
# Upload Section
# ------------------------------

st.subheader("📁 Upload Study Material")

uploaded_file = st.file_uploader(
    "Upload syllabus or textbook chapter",
    type=["pdf", "txt"],
    help="Recommended limit: 25MB"
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

            st.success("Document processed successfully!")

elif uploaded_file and not GROQ_API_KEY:

    st.error(
        "Server configuration error: GROQ_API_KEY missing."
    )


# ------------------------------
# Topic Focus
# ------------------------------

st.subheader("🎯 Refine Focus (Optional)")

topic_input = st.text_input(
    "Enter a specific topic",
    placeholder="Neural Networks, Recursion, Laws of Motion..."
)

st.caption("Leave blank to generate questions from the entire document.")


# ------------------------------
# Question Generation
# ------------------------------

if st.session_state.vectorstore and GROQ_API_KEY:

    if st.button("🚀 Generate Exam Questions"):

        with st.spinner("Generating questions..."):

            query = topic_input if topic_input else "important concepts"

            chunks = retrieve_chunks(
                st.session_state.vectorstore,
                query
            )

            questions = generate_questions(
                chunks=chunks,
                difficulty=difficulty,
                language=language,
                num_questions=num_questions,
                api_key=GROQ_API_KEY,
                topic=topic_input,
                model=MODEL_NAME
            )

            if topic_input:
                st.session_state.tracker = update_tracker(
                    st.session_state.tracker,
                    topic_input
                )

            st.session_state.history.append({
                "topic": topic_input or "Overview",
                "difficulty": difficulty,
                "language": language,
                "questions": questions
            })


# ------------------------------
# Display Output
# ------------------------------

if st.session_state.history:

    latest = st.session_state.history[-1]

    st.subheader(f"📝 Practice Questions — {latest['topic']}")

    st.caption(
        f"Difficulty: {latest['difficulty']} | Language: {latest['language']}"
    )

    st.markdown(latest["questions"])

    if len(st.session_state.history) > 1:

        with st.expander("📚 Previous Sessions"):

            for session in reversed(st.session_state.history[:-1]):

                st.markdown(
                    f"**Topic:** {session['topic']} | "
                    f"{session['difficulty']} | "
                    f"{session['language']}"
                )

                st.markdown(session["questions"])
                st.divider()

elif not st.session_state.vectorstore:

    st.info("Upload a document to start generating questions.")