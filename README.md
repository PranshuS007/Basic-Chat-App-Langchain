# Conversational AI Chatbot with FastAPI + Streamlit + LangChain (Groq)

## 📄 Overview

This project is a fully containerized conversational chatbot built with:

- **LangChain** using **Groq's LLM (LLaMA 3)**
- **Streamlit** for a sleek chat UI
- **FastAPI** as a backend API server
- **Docker** for packaging
- **Kubernetes (Kind)** for deployment and scalability

---

## 💡 Architecture

```
                +-----------------+
                |  Streamlit UI   |
                |-----------------|
                | chat_ui.py      |        
                | [NodePort:8501] |
                +--------+--------+
                         |
                         | REST call to /chat
                         v
                +--------+--------+
                |  FastAPI Server  |
                |-----------------|
                | main.py         |
                | /chat endpoint  |
                | [ClusterIP:8000]|
                +--------+--------+
                         |
                         v
            +------------+-------------+
            | LangChain + Groq LLM     |
            | ConversationChain        |
            | ConversationBufferMemory|
            +--------------------------+
```

---

## 🌐 Tech Stack

- **LangChain**: Memory + Prompt + Groq LLM
- **Groq API**: Ultra-fast inference with LLaMA3
- **Streamlit**: UI frontend
- **FastAPI**: API backend
- **Docker** + **Docker Compose**
- **Kubernetes**: Multi-container orchestration with Kind

---

## 💡 Folder Structure

```
chat-app/
├── app/
│   ├── main.py               # FastAPI app
│   ├── chat_ui.py            # Streamlit frontend
│   ├── chat_engine.py        # LangChain core logic
│   ├── requirements.txt
├── Dockerfile.fastapi
├── Dockerfile.streamlit
├── docker-compose.yml
├── .env                      # Contains GROQ_API_KEY
├── k8s/
│   ├── env-secret.yaml
│   ├── fastapi-deployment.yaml
│   ├── fastapi-service.yaml
│   ├── streamlit-deployment.yaml
│   ├── streamlit-service.yaml
```

---

## 🎓 LangChain Logic (chat\_engine.py)

```python
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

llm = ChatGroq(model="llama3-8b-8192", api_key=api_key)
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory, verbose=True)
```

- **ChatGroq**: Accesses Groq's LLaMA model
- **ConversationBufferMemory**: Keeps track of user & AI messages
- **ConversationChain**: Chains LLM with memory

---

## 🌐 Streamlit UI (chat\_ui.py)

```python
st.title("Chatbot")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Type your message...")
if user_input:
    response = conversation.run(input=user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))
```

- Allows multi-turn chat with session state
- Uses `chat_input` and `chat_message`
- Sends message to FastAPI `/chat` (optional)

---

## 🚀 FastAPI (main.py)

```python
from fastapi import FastAPI, Request
from app.chat_engine import conversation

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("query")
    response = conversation.run(input=prompt)
    return {"response": response}
```

- Exposes `/chat` API endpoint
- Forwards prompt to LangChain
- Returns AI response

---

## 📁 Docker Setup

### Dockerfile.streamlit

```Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY app/requirements.txt .
RUN pip install -r requirements.txt
COPY app/ .
CMD ["streamlit", "run", "chat_ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Dockerfile.fastapi

```Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY app/requirements.txt .
RUN pip install -r requirements.txt
COPY app/ .
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]
```

### docker-compose.yml

```yaml
services:
  streamlit:
    build:
      context: .
      dockerfile: Dockerfile.streamlit
    ports:
      - "8501:8501"
    env_file: .env

  fastapi:
    build:
      context: .
      dockerfile: Dockerfile.fastapi
    ports:
      - "8000:8000"
    env_file: .env
```

---

## 🚧 Kubernetes Deployment (with Kind)

### Steps:

1. Create Docker images
2. Load into kind:
   ```bash
   kind load docker-image streamlit-chatbot:latest
   kind load docker-image fastapi-server:latest
   ```
3. Apply:
   ```bash
   kubectl apply -f k8s/env-secret.yaml
   kubectl apply -f k8s/fastapi-deployment.yaml
   kubectl apply -f k8s/streamlit-deployment.yaml
   kubectl apply -f k8s/fastapi-service.yaml
   kubectl apply -f k8s/streamlit-service.yaml
   ```

### Expose via Port Forwarding

```bash
kubectl port-forward service/streamlit-service 8501:8501
kubectl port-forward service/fastapi-service 8000:8000
```

---

## 📃 Secrets (env-secret.yaml)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: chatbot-env
stringData:
  GROQ_API_KEY: "your_key_here"
```

Used in:

```yaml
envFrom:
  - secretRef:
      name: chatbot-env
```

---

## ✨ Future Enhancements

- Add multiple LLMs (e.g., OpenAI, Anthropic) via dropdown
- Chat history persistence using Redis / Postgres
- Auth & user sessions
- Multi-tab memory
- Streaming response

---

## 📄 Final Note

This project gives you a scalable, multi-service chatbot using best practices in:

- MLOps (Docker, K8s)
- Modern frontend (Streamlit)
- Async APIs (FastAPI)
- Cutting-edge LLM (Groq)

Let me know if you'd like PDF or GitHub README version.

