from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = FastAPI()

access = os.environ.get("ACCESS_TOKEN")
secret_key = os.environ.get("SECRET_KEY")

line_bot_api = LineBotApi(access)
handler = WebhookParser(secret_key)

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
            line_bot_api.push_message(line_user_id, TextSendMessage(text=SWOn))
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

SWOn = 'デスクトップの電源を[ON]にしました'
falseWords = "ん？"
lightOnWords = ["パソコンつけて", "パソコンおん", "パソコン付けて", "パソコン点けて", "パソコン付けといて", "pcon", "ぱそこんおん", "パソコンオン", "パソコン"]
