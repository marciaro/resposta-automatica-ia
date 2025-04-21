from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import openai
import os

def buscar_respostas(query, base_conhecimento, top_k=3):
    documentos = [doc["conteudo"] for doc in base_conhecimento]
    tfidf = TfidfVectorizer().fit_transform([query] + documentos)
    cosine_sim = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()
    top_indices = cosine_sim.argsort()[-top_k:][::-1]
    return [base_conhecimento[i] for i in top_indices]

def gerar_prompt(pergunta, documentos_relevantes):
    contexto = "\n\n".join([f"{doc['titulo']}:\n{doc['conteudo']}" for doc in documentos_relevantes])
    prompt = f"""
Base de conhecimento:
{contexto}

Pergunta do usuário:
{pergunta}

Com base na base de conhecimento acima, responda de forma clara e objetiva:
"""
    return prompt

def chamar_gpt(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente que responde perguntas com base em uma base de conhecimento interna."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response["choices"][0]["message"]["content"].strip()

def salvar_feedback(pergunta, resposta, relevancia, comentario):
    with open("feedback.log", "a", encoding="utf-8") as f:
        f.write(f"{pergunta}|{resposta}|{relevancia}|{comentario}\n")