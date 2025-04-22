from flask import Flask, request, jsonify, render_template
import json
import os
from utils import buscar_respostas, montar_prompt, chamar_gpt, salvar_feedback
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

with open("base_conhecimento.json", "r", encoding="utf-8") as f:
    base_conhecimento = json.load(f)

@app.route("/pergunta", methods=["POST"])
def responder():
    data = request.json
    pergunta = data.get("pergunta")
    docs_relevantes = buscar_respostas(pergunta, base_conhecimento)
    prompt = montar_prompt(pergunta, docs_relevantes)
    resposta = chamar_gpt(prompt)
    return jsonify({"resposta": resposta})

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json
    salvar_feedback(data["pergunta"], data["resposta"], data["relevancia"], data["comentario"])
    return jsonify({"status": "feedback recebido"})

@app.route("/")
def index():
    return render_template ("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)