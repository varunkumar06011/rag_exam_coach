# Deployment Guide for RAG Exam Coach

You can easily deploy the RAG Exam Coach app publicly on multiple cloud platforms. Below are structured instructions to deploy it using [Streamlit Community Cloud](https://streamlit.io/cloud), [HuggingFace Spaces](https://huggingface.co/spaces), or [Render](https://render.com).

## Prerequisites
Before you start, push your code to a public or private GitHub repository.

### Ensure your GitHub repo has these core files:
- `requirements.txt`
- `app.py`
- `src/` folder
- `runtime.txt` (Required for Render)
- `Procfile` (Required for Render)

---

## Option 1: Deploy on Streamlit Community Cloud (Recommended & Easiest)

Streamlit Community Cloud is highly optimized for Streamlit apps and completely free.

1. Go to [share.streamlit.io](https://share.streamlit.io/).
2. Log in with your GitHub account.
3. Click on the **New app** button.
4. Select the GitHub repository where you uploaded the code.
5. In the "Main file path" section, type: `app.py`.
6. Click **Advanced settings**.
7. In the "Secrets" field, paste your Groq API key to match the structure in your `.streamlit/secrets.toml.example` file:
   ```toml
   [secret]
   GROQ_API_KEY = "gsk_your_actual_groq_api_key_here"
   ```
8. Click **Deploy!** 

Your app will go live at a custom URL (e.g., `https://your-app-repo-name.streamlit.app`).

---

## Option 2: Deploy on HuggingFace Spaces

HuggingFace Spaces is great for AI/RAG applications and offers completely free Streamlit instance hosting.

1. Create an account and log in to [Hugging Face](https://huggingface.co/).
2. Navigate to your Spaces profile or click **New Space**.
3. Fill in the following:
   - **Space name**: e.g., `rag-exam-coach`
   - **License**: Choose your preferred license (e.g., `mit` or `apache-2.0`).
   - **Select the Space SDK**: Choose **Streamlit**.
   - **Space Hardware**: Free CPU basic is sufficient.
4. Click **Create space**.
5. Once created, clone the Space repository locally or upload your files directly through the Hugging Face web interface. Upload:
   - `app.py`
   - `requirements.txt`
   - `src/` folder
6. Go to the **Settings** tab on your Space.
7. Scroll down to **Variables and secrets**. 
8. Click **New secret**.
   - **Name**: `GROQ_API_KEY`
   - **Value**: `gsk_your_actual_groq_api_key_here`
9. Hugging Face will automatically detect `requirements.txt` and `app.py` and start building your application.

---

## Option 3: Deploy on Render

If you need a more traditional PaaS (Platform as a Service) solution, Render is a great option.

1. Go to [render.com](https://render.com/) and create an account.
2. Go to your Dashboard and click **New +** -> **Web Service**.
3. Select **Build and deploy from a Git repository**.
4. Connect the GitHub repository containing your application code.
5. Fill in the settings:
   - **Name**: e.g., `rag-exam-coach`
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: Wait to leave as defaults or enter `web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0` (Render will automatically detect this via the `Procfile`).
6. Scroll down and click **Advanced**.
7. Under **Environment Variables**, click **Add Environment Variable**:
   - **Key**: `GROQ_API_KEY`
   - **Value**: `gsk_your_actual_groq_api_key_here`
8. Click **Create Web Service**. 
9. Render will deploy the application and provide a public URL (e.g., `https://rag-exam-coach.onrender.com`).

---
Once deployed via any platform, you can go to your live link, upload a PDF/TXT textbook document, provide your Groq API key in the side-bar (if you don't use the Secrets setting directly on the server), and start studying!
