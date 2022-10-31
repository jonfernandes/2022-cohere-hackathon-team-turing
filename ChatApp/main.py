import json
import datetime
from re import M
from fastapi import (
    FastAPI, WebSocket, WebSocketDisconnect, Request, Response
)
from typing import List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import itertools
from pathlib import Path

from .ai_manager import AIManager
from .ai_manager import API_KEY

BASE_DIR = Path(__file__).resolve().parent

customer_support_chat = []
customer_chat = []
call_log = []
customer_support_user = 'Jack Daws'

def create_logs(outp):
    chat_time = f'{datetime.datetime.today():%Y-%m-%d %H:%M}'
    output_filename = f'{datetime.datetime.today():%Y-%m-%d %H%M}.md'
    positive_confidence = round(outp[0].labels['positive'].confidence, 2)
    negative_confidence = round(outp[0].labels['negative'].confidence, 2)
    neutral_confidence = round(outp[0].labels['neutral'].confidence, 2)
    prediction = outp[0].prediction
    prediction_confidence = rount(outp[0].confidence, 2)
    with open(Path().cwd()/'ChatApp'/'call_logs'/f'{output_filename}', 'wt') as file:
        file.write(f'# Chat log ({chat_time})\n')
        file.write(f'### Support call worker ID: Jack Daws\n')
        file.write(f'### Customer ID:\n')
        file.write(f"### Call sentiment: {prediction}({prediction_confidence}) [positive({positive_confidence}), negative({negative_confidence}), neutral({neutral_confidence})\n")
        file.write(f'### Confidence:\n')
        file.write(f'### Customer chat log: \n')
        file.write(f'---\n')
        file.write(f'## Details\n')
        for line in call_log:
            line = line + '<br>'
            file.write(line)

app = FastAPI()

app.mount(
    "/static", StaticFiles(directory=str(Path(BASE_DIR, 'static'))), name='static')

# locate templates
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

#ai_manager = AIManager('04phuWRJP2o2r7NApFvq5BBbNZahzNwQrDSNXhuR')  # add API key in the quotation marks
ai_manager = AIManager(API_KEY)

@app.get("/")
def get_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/customer-chat")
def get_customerChat(request: Request):
    return templates.TemplateResponse("customerChat.html", {"request": request})


@app.get("/customer-support")
def get_customerSupportChat(request: Request):
    return templates.TemplateResponse("customerSupportChat.html", {"request": request})


class RegisterValidator(BaseModel):
    username: str

    class Config:
        orm_mode = True


class SocketManager:
    def __init__(self):
        self.active_connections: List[(WebSocket, str)] = []

    async def connect(self, websocket: WebSocket, user: str):
        await websocket.accept()
        self.active_connections.append((websocket, user))

    def disconnect(self, websocket: WebSocket, user: str):
        self.active_connections.remove((websocket, user))

    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            await connection[0].send_json(data)


manager = SocketManager()


def postMessage(msg):
    ...


templates.env.globals.update(postMessage=postMessage)


async def handleCustomerSupport(data):
    await manager.broadcast(data)


async def handleCustomer(data):
    await manager.broadcast(data)

    df = ai_manager.answer_message(data['message'])
    msgs = []

    questions = df['question'].to_list()
    distances = df['distance'].to_list()

    for q, d in zip(questions, distances):
        msgs.append({'question': q, 'distance': d})

    data = {
        'sender': 'Customer',
        'type': 'multichoice',
        'messages': msgs
    }
    await manager.broadcast(data)


async def handleCustomerSupportBot(data):
    await manager.broadcast(data)


@app.websocket("/api/chat/{sender}")
async def chat(websocket: WebSocket, sender):

    if sender:
        await manager.connect(websocket, sender)
        response = {
            "sender": sender,
            "message": "got connected"
        }
        try:
            await manager.broadcast(response)
            while True:
                data = await websocket.receive_json()

                if data["sender"] == 'Customer Support':
                    customer_support_chat.append(data["message"])
                    call_log.append(f'**Customer Support:** {data["message"]}')
                else:
                    customer_chat.append(data["message"])
                    call_log.append(f'**Customer:** {data["message"]}')                
                match sender:
                    case "Customer Support":
                        await handleCustomerSupport(data)

                    case "Customer":
                        await handleCustomer(data)

                    case "Customer Support Bot":
                        await handleCustomerSupportBot(data)

        except WebSocketDisconnect:
            manager.disconnect(websocket, sender)
            response['message'] = "left"
            outp = ai_manager.sentiment_analysis('. '.join(customer_chat))
            create_logs(outp)
            await manager.broadcast(response)
