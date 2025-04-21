# 🤖 Sistema de Respostas Automáticas com IA

Este projeto utiliza Flask + OpenAI + TF-IDF para responder dúvidas de usuários com base em uma base de conhecimento interna. A aplicação roda em containers usando Docker Compose.

---

## 🚀 Como rodar o projeto

### Pré-requisitos
- Docker
- Docker Compose
- Variável de ambiente `OPENAI_API_KEY` com sua chave da OpenAI

### Passos

```bash
# Clone o repositório
$ git clone seu-repo-aqui
$ cd nome-do-projeto

# Crie o arquivo .env com sua chave da OpenAI
$ echo "OPENAI_API_KEY=sua-chave-aqui" > .env

# Torne os scripts executáveis
$ chmod +x start.sh stop.sh

# Suba os containers
$ ./start.sh
```

A API estará disponível em `http://localhost:5000`

---

### 📴 Encerrar a aplicação

```bash
./stop.sh
```

---

## 📚 Endpoints

### `POST /pergunta`
**Descrição:** Recebe uma pergunta e retorna a resposta baseada na base de conhecimento.

**Payload:**
```json
{
  "pergunta": "Como faço para resetar minha senha?"
}
```
**Resposta:**
```json
{
  "resposta": "Para resetar sua senha, clique em..."
}
```

### `POST /feedback`
**Descrição:** Envia feedback sobre a resposta recebida.

**Payload:**
```json
{
  "pergunta": "Como faço para resetar minha senha?",
  "resposta": "Texto da resposta gerada",
  "relevancia": 4,
  "comentario": "Foi útil, mas poderia ser mais detalhado."
}
```

---

## 🧱 Estrutura de arquivos
```
.
├── base_conhecimento.json
├── main.py
├── utils.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── feedback.log
├── .env.example
├── start.sh
└── stop.sh
```

---

## 🛠 Melhorias futuras
- Armazenar feedbacks em banco de dados
- Autenticação de API
- Interface web
- Treinamento com feedbacks coletados

---

Feito com 💻 + ☕