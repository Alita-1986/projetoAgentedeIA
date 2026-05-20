
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

# Modelo gratuito via Groq
llm = chat = ChatGroq(
    temperature=0.7,
    model="llama-3.3-70b-versatile"

)

# Personalidade do seu companheiro
SYSTEM_PROMPT = """
Você é Sara, uma IA simpática,  curiosa e pacifica.
Responda SEMPRE em português brasileiro de forma informal.
Máximo 2 frases por resposta. Use emojis às vezes.
Nunca diga que é uma IA — você é simplesmente Sara!
"""

def get_response(user_message: str, history: list) -> str:
    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    
    # Adiciona histórico da conversa
    for msg in history[-6:]:  # últimas 6 mensagens
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
    
    messages.append(HumanMessage(content=user_message))
    
    response = llm.invoke(messages)
    return response.content