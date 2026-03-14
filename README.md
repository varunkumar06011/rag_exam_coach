# 🎓 Finish Task – Smart Study Assistant

A Retrieval Augmented Generation (RAG) powered smart study assistant.  
Upload any syllabus or textbook chapter and instantly generate **difficulty-rated exam questions in English or Telugu**. 

*(Note: Newly updated with a modern, student-friendly card UI theme!)*

---

## ✨ Features

- 📄 **Modern UI/UX** — Clean, card-based student-friendly interface.
- 🧠 **RAG Pipeline** — Retrieves the most relevant content before generating questions.
- 🎯 **Difficulty Levels** — Easy / Medium / Hard questions tailored to exam patterns.
- 🗣️ **Telugu Language Support** — Get questions generated in Telugu (తెలుగు).
- 📊 **Weak Topic Tracker** — Tracks which topics you revisit most (your weak areas).
- 💾 **Session History** — View questions from previous sessions in the same run.

---

## 🚀 How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/rag-exam-coach.git
cd rag-exam-coach
```

### 2. Create and Activate a Virtual Environment
**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up Environment Variables
Copy the `.env.example` to create your own `.env` file or Streamlit secrets file:
```bash
cp .env.example .env
```
*(Alternatively, enter your API key directly in the Streamlit app sidebar)*

### 5. Run the app
```bash
streamlit run app.py
```

### 6. Enter your Groq API Key
Get a free key at [console.groq.com](https://console.groq.com)  
Make sure you have placed your key in `.env` or `.streamlit/secrets.toml` as described in Step 4.

---

## 🗂️ Project Structure

```
rag_exam_coach/
│
├── app.py                  # Main Streamlit UI
├── requirements.txt        # Dependencies
├── README.md
│
├── src/
│   ├── rag_pipeline.py     # Document chunking, embedding, FAISS retrieval
│   ├── question_generator.py  # Groq LLM question generation
│   ├── topic_tracker.py    # Weak topic tracking logic
│   └── utils.py            # PDF extraction, helpers
│
└── data/
    └── topic_tracker.json  # Auto-generated — stores your weak topics
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| LLM | Groq API (LLaMA3-8B) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Store | FAISS |
| PDF Parsing | PyPDF2 |
| Language | Python 3.10+ |

---

## 🌐 Deployment

Please read the newly provided [DEPLOYMENT.md](DEPLOYMENT.md) guide for comprehensive, step-by-step instructions on how to deploy this application to:
- **Streamlit Community Cloud**
- **HuggingFace Spaces**
- **Render**

---

## 📌 Notes

- Works best with **text-based PDFs** (not scanned images)
- Telugu output quality depends on the LLM — LLaMA3 handles it reasonably well
- Weak topic tracker resets when you click "Reset Tracker" in the sidebar

---

## 👨‍💻 Built By

**Nagamothu Varun Kumar**  
B.Tech CSE (AI) — Parul University  
[GitHub](https://github.com/varunkumar06011) | [LinkedIn](https://linkedin.com/in/nagumothu-varunkumar-25616030a)
