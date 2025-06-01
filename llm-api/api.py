from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Callable, Dict
from myagent.crew import MyAgent
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import os

# Carregar variáveis de ambiente
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

app = FastAPI()

class WhatsAppMessage(BaseModel):
    from_: str
    name: Optional[str]
    message: str
    from_me: bool

# === Funções dos comandos ===
def comando_teste(_: WhatsAppMessage) -> str:
    return "🧪 Comando !teste processado com sucesso!"

def comando_hora(_: WhatsAppMessage) -> str:
    return f"⏰ Agora são {datetime.now().strftime('%H:%M:%S')}"

def comando_comands(_: WhatsAppMessage) -> str:
    return "📋 Comandos disponíveis:\n" + "\n".join(comando_handlers.keys())

def comando_agent(data: WhatsAppMessage) -> str:
    message = data.message[len("!agent"):].strip()
    from_me = 'Mestre Pedro' if data.from_me else 'Outra pessoa'
    result = MyAgent().crew().kickoff(inputs={"user_input": message, "message_from":from_me})

    return result.raw if hasattr(f'🤖: {result}', "raw") else str(f'🤖:{result}')

# === Dicionário de comandos ===
comando_handlers: Dict[str, Callable[[WhatsAppMessage], str]] = {
    "!test": comando_teste,
    "!hora": comando_hora,
    "!comands": comando_comands,
    "!agent": comando_agent,
}

@app.post("/webhook")
async def receive_whatsapp_message(data: WhatsAppMessage):
    print(f"📩 Comando recebido de {data.name or data.from_}: {data.message}, {data.from_me}")

    # Identifica o comando base
    comando_base = data.message.split()[0]  # ex: '!agent', '!teste'

    if comando_base in comando_handlers:
        try:
            resposta = comando_handlers[comando_base](data)
            return {"reply": resposta}
        except Exception as e:
            return {"reply": f"❌ Erro ao processar comando {comando_base}: {str(e)}"}
