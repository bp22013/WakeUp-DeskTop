from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = FastAPI()

# 環境変数設定
ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN", "Hfyt/ngdfr5WqH/e7E9Yfv+2gchmHoBWE+gHoE754C9pEk1mnriU5iIlJ/3lLWCZH77Q9k+qB8u1FlgbxrYJxSvjLuGMkDbb1iN2qgyGQW4XIZu09JmfZ1468zXtFFnvRfqjfWqzrintM1P0jCRNuAdB04t89/1O/w1cDnyilFU=")
SECRET = os.getenv("LINE_SECRET", "3b8aa613029acdf995cfe6abd3018965")

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookParser(SECRET)

@app.post("/")
async def callback(request: Request):
    # ヘッダー
    signature = request.headers.get('X-Line-Signature', '')
    
    # リクエストボディ
    body = await request.body()
    body_str = body.decode('utf-8')
    print(body_str)
    
    try: 
        events = handler.parse(body_str, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        
        text = event.message.text
        line_user_id = event.source.user_id
        global a
        if text in lightOnWords:
            line_bot_api.push_message(line_user_id, TextSendMessage(text=lightOn))
            a = 1
        else:
            line_bot_api.push_message(line_user_id, TextSendMessage(text=falseWords))
    
    return JSONResponse(content={"status": "OK"})

# フラグ用グローバル変数
a = 0

@app.get("/")
async def handle_get_request():
    global a
    b = a
    a = 0
    print("accept_" + str(b))
    # GETリクエスト時のパラメータをbot経由で通知
    # line_bot_api.push_message("Ufc2f9581f7270b02bdf52f7ae30c337f", TextSendMessage(text="accept_" + str(b)))
    return {"message": f"%%%{b}%%%"}

lightOn = '照明を[ON]にしました'
SWOn = 'デスクトップの電源を[ON]にしました'
falseWords = "ん？"
lightOnWords = ["パソコンつけて", "パソコンおん", "パソコン付けて", "パソコン点けて", "パソコン付けといて", "pcon", "ぱそこんおん", "パソコンオン", "パソコン"]