"""
Question Generator — uses Groq LLM API to generate exam questions
from retrieved RAG chunks, with difficulty levels and language support.
"""

from groq import Groq


DIFFICULTY_INSTRUCTIONS = {
    "Easy": (
        "Generate simple recall and definition-based questions. "
        "Focus on 'What is', 'Define', 'List' type questions."
    ),
    "Medium": (
        "Generate application and understanding-based questions. "
        "Focus on 'Explain', 'How does', 'Compare' type questions."
    ),
    "Hard": (
        "Generate analysis and evaluation-based questions. "
        "Focus on 'Analyze', 'Evaluate', 'Design a solution for' type questions."
    ),
}

LANGUAGE_INSTRUCTIONS = {
    "English": "Respond entirely in English.",
    "Telugu": (
        "Respond entirely in Telugu language (తెలుగు). "
        "Write all questions and answers in Telugu script. "
        "Use simple, clear Telugu that a college student would understand."
    ),
}


def generate_questions(
    chunks: str,
    difficulty: str,
    language: str,
    num_questions: int,
    api_key: str,
    topic: str = None,
    model: str = "llama-3.1-8b-instant",
) -> str:
    """
    Generate exam questions from document chunks using Groq LLM.

    Args:
        chunks: Retrieved text from vectorstore
        difficulty: Easy / Medium / Hard
        language: English / Telugu
        num_questions: How many questions to generate
        api_key: Groq API key
        topic: Optional specific topic to focus on

    Returns:
        Formatted string of questions
    """
    client = Groq(api_key=api_key)

    topic_line = f"Focus specifically on the topic: **{topic}**." if topic else "Cover the key concepts from the content."

    system_prompt = f"""You are an expert exam question generator for Indian engineering college students.
{LANGUAGE_INSTRUCTIONS[language]}
{DIFFICULTY_INSTRUCTIONS[difficulty]}

Format your response as a numbered list of questions.
For each question also provide:
- A short hint or expected answer approach (1-2 lines)
- The topic/concept it tests

Make questions relevant to university-level examinations."""

    user_prompt = f"""Based on the following study material, generate exactly {num_questions} exam questions.
{topic_line}
Difficulty Level: {difficulty}

--- STUDY MATERIAL ---
{chunks}
--- END OF MATERIAL ---

Generate {num_questions} well-structured exam questions now."""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=2048,
        )
        return response.choices[0].message.content

    except Exception as e:
        error_msg = str(e)
        if "organization_restricted" in error_msg:
            return (
                "⚠️ **Groq API Access Restricted**: The current API key belongs to an organization that is restricted. "
                "This often happens if the account is under review or has billing issues.\n\n"
                "**How to fix:**\n"
                "1. Go to [Groq Console](https://console.groq.com/keys) and generate your own API key.\n"
                "2. Paste it into the 'Override Groq API Key' box in the sidebar.\n"
                "3. Try generating questions again."
            )
        return f"⚠️ Error generating questions: {error_msg}\n\nPlease check your Groq API key and try again."
