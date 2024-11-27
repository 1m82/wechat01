from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 设置模板目录
templates = Jinja2Templates(directory="templates")

# 配置信息（建议使用环境变量存储）
PHONE = "1**********"  # 车主电话
WXPUSHER_APP_TOKEN = "AT_****************"  # WxPusher APP Token
WXPUSHER_UIDS = ["UID_****************"]  # 接收者的UID

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "phone": PHONE,
            "wxpusher_app_token": WXPUSHER_APP_TOKEN,
            "wxpusher_uids": WXPUSHER_UIDS
        }
    )

@app.post("/send_notification")
async def send_notification(request: Request):
    import requests
    data = await request.json()
    message = data.get("message")
    
    url = "https://wxpusher.zjiecode.com/api/send/message"
    wx_data = {
        "appToken": WXPUSHER_APP_TOKEN,
        "content": message,
        "contentType": 1,
        "uids": WXPUSHER_UIDS
    }
    
    try:
        response = requests.post(url, json=wx_data)
        result = response.json()
        if result.get("code") == 1000:
            return {"success": True, "message": "通知发送成功！"}
        else:
            return {"success": False, "message": f"发送失败：{result.get('msg')}"}
    except Exception as e:
        return {"success": False, "message": f"发送错误：{str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
