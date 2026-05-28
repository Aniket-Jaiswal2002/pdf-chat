import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_prompt(question: str, context_chunks: list[dict]) -> str:
    """
    Build a prompt that includes the retrieved chunks as context.
    This is the core of RAG - we give the LLM the relevant PDF sections
    so it can answer based on the document, not just its training data.
    """
    context = "\n\n---\n\n".join([c["chunk"] for c in context_chunks])
    
    prompt = f"""You are a helpful assistant that answers questions based on the provided document context.

CONTEXT FROM DOCUMENT:
{context}

QUESTION: {question}

Instructions:
- Answer based ONLY on the context provided above
- If the answer is not in the context, say "I couldn't find that in the document"
- Be concise and clear
- Mention which part of the document your answer comes from

ANSWER:"""
    return prompt

def get_answer(question: str, context_chunks: list[dict]) -> str:
    """Send the prompt to Groq LLaMA 3 and get an answer."""
    prompt = build_prompt(question, context_chunks)
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,  # low = more factual, less creative
        max_tokens=512
    )
    
    return response.choices[0].message.content