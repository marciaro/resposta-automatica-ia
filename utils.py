import json
import os
import openai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Novo cliente compatível com openai >= 1.0.0
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Carrega a base de conhecimento
with open("base_conhecimento.json", "r", encoding="utf-8") as f:
    base_conhecimento = json.load(f)

# Pré-processa os textos para TF-IDF
textos = [f'{item["pergunta"]} {item["resposta"]}' for item in base_conhecimento]
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(textos)

def buscar_respostas(pergunta, base_conhecimento, top_n=3):
    textos = [f'{item["pergunta"]} {item["resposta"]}' for item in base_conhecimento]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(textos)
    pergunta_vec = vectorizer.transform([pergunta])
    similaridades = cosine_similarity(pergunta_vec, tfidf_matrix).flatten()
    indices = similaridades.argsort()[::-1][:top_n]
    resultados = [textos[i] for i in indices]
    return resultados

def montar_prompt(pergunta, contexto):
    prompt = [
        {"role": "system", "content": "Você é um assistente especializado em suporte técnico e atendimento ao cliente. Responda de forma clara e objetiva."},
        {"role": "user", "content": f"Contexto:\n{contexto}\n\nPergunta: {pergunta}"}
    ]
    return prompt

def chamar_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=0.7
    )
    return response.choices[0].message.content


def salvar_feedback(pergunta, resposta, relevancia, comentario):
    with open("feedback.log", "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "pergunta": pergunta,
            "resposta": resposta,
            "relevancia": relevancia,
            "comentario": comentario
        }, ensure_ascii=False) + "\n")
