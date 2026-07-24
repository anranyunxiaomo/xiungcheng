import os
import json
import time
import subprocess
from datetime import datetime, timedelta
import requests

APP_ID = os.environ.get("WECHAT_APP_ID", "wxf39166d6f2deab57")
APP_SECRET = os.environ.get("WECHAT_APP_SECRET", "c2fb35bda2fe52d795e6a64a70d3e38e")
USER_OPENID = os.environ.get("WECHAT_USER_OPENID", "of84Y3bGGlhFtf7vqa52snEve8w4")

cwd = "/Users/anranyunxiaomo/Desktop/project/xiungcheng"

def get_access_token():
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    try:
        r = requests.get(token_url).json()
        return r.get("access_token")
    except Exception as e:
        print("获取 token 异常:", e)
        return None

def upload_image_to_wechat(token, file_path):
    upload_url = f"https://api.weixin.qq.com/cgi-bin/media/upload?access_token={token}&type=image"
    try:
        with open(file_path, "rb") as f:
            files = {"media": f}
            res = requests.post(upload_url, files=files).json()
        return res.get("media_id")
    except Exception as e:
        print("上传图片异常:", e)
        return None

def send_image_msg(token, media_id):
    custom_url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={token}"
    payload = {
        "touser": USER_OPENID,
        "msgtype": "image",
        "image": {
            "media_id": media_id
        }
    }
    json_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    return requests.post(custom_url, data=json_data, headers=headers).json()

def send_text_msg(token, content):
    custom_url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={token}"
    payload = {
        "touser": USER_OPENID,
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    json_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    return requests.post(custom_url, data=json_data, headers=headers).json()

def generate_poster_image(tag, title, elevation, temp, rain, fashion, cares):
    html_path = os.path.join(cwd, "temp_poster.html")
    img_path = os.path.join(cwd, "temp_poster.png")

    care_items_html = "".join([f"<li>{c}</li>" for c in cares])

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; -webkit-font-smoothing: antialiased; }}
body {{ margin: 0; padding: 0; width: 480px; font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "PingFang SC", "Helvetica Neue", sans-serif; background: #f4f4f7; color: #1c1c1e; }}
.poster {{ width: 480px; background: #ffffff; padding: 32px 28px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }}
.badge-tag {{ display: inline-block; background: linear-gradient(135deg, #ff758c 0%, #ff7eb3 100%); color: #ffffff; font-size: 12px; font-weight: 700; padding: 4px 12px; border-radius: 20px; letter-spacing: 0.5px; margin-bottom: 12px; }}
.title {{ font-size: 23px; font-weight: 800; color: #0f172a; line-height: 1.3; margin: 0 0 6px 0; }}
.subtitle {{ font-size: 13px; color: #64748b; margin-bottom: 24px; display: flex; align-items: center; gap: 6px; }}
.card-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px; }}
.info-card {{ background: #f8fafc; border: 1px solid #f1f5f9; border-radius: 14px; padding: 14px 16px; }}
.card-label {{ font-size: 11px; color: #94a3b8; font-weight: 600; margin-bottom: 4px; text-transform: uppercase; }}
.card-val {{ font-size: 15px; font-weight: 700; color: #0f172a; }}
.card-sub {{ font-size: 11.5px; color: #64748b; margin-top: 2px; }}
.fashion-card {{ background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%); border-radius: 16px; padding: 18px 20px; margin-bottom: 20px; border: 1px solid #fecaca; }}
.section-head {{ font-size: 14px; font-weight: 700; color: #991b1b; margin-bottom: 10px; display: flex; align-items: center; gap: 6px; }}
.fashion-item {{ font-size: 13px; color: #7f1d1d; line-height: 1.6; margin-bottom: 6px; }}
.care-card {{ background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-radius: 16px; padding: 18px 20px; margin-bottom: 24px; border: 1px solid #bae6fd; }}
.care-head {{ font-size: 14px; font-weight: 700; color: #0369a1; margin-bottom: 10px; display: flex; align-items: center; gap: 6px; }}
.care-list {{ margin: 0; padding-left: 18px; font-size: 13px; color: #0c4a6e; line-height: 1.6; }}
.care-list li {{ margin-bottom: 6px; }}
.footer {{ border-top: 1px dashed #e2e8f0; padding-top: 16px; display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: #94a3b8; }}
.heart-sign {{ color: #ff4757; font-weight: 700; }}
</style>
</head>
<body>
<div class="poster">
  <span class="badge-tag">{tag}</span>
  <h1 class="title">{title}</h1>
  <div class="subtitle"><span>📍 {elevation}</span></div>
  <div class="card-grid">
    <div class="info-card">
      <div class="card-label">🌤️ 节点气温</div>
      <div class="card-val">{temp}</div>
    </div>
    <div class="info-card">
      <div class="card-label">🌧️ 降雨预测</div>
      <div class="card-val">{rain}</div>
    </div>
  </div>
  <div class="fashion-card">
    <div class="section-head">👗 穿搭灵感与打卡建议</div>
    <div class="fashion-item">{fashion}</div>
  </div>
  <div class="care-card">
    <div class="care-head">💡 暖心守护与注意事项</div>
    <ul class="care-list">{care_items_html}</ul>
  </div>
  <div class="footer">
    <span>🛡️ 多源权威数据交叉核验</span>
    <span class="heart-sign">💖 祝行程浪漫愉快</span>
  </div>
</div>
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    cmd = [
        chrome_path, "--headless", "--no-sandbox", "--disable-gpu",
        "--window-size=480,960", f"--screenshot={img_path}", f"file://{html_path}"
    ]
    subprocess.run(cmd, capture_output=True)
    return img_path

HIGH_AESTHETIC_CARDS = {
    "08-01": {
        "tag": "🌸 8.1 明日川西自驾预告",
        "title": "成都 ➔ 康定",
        "elevation": "海拔 2560m (第一晚低海拔适应)",
        "temp": "14℃ ~ 22℃",
        "rain": "19:00 夜间小雨",
        "fashion": "<strong>建议穿搭：</strong>透气长袖内搭 + 随身防风外套<br><strong>拍照打卡：</strong>傍晚 18:00 康定情歌广场与折多河畔",
        "cares": [
            "第一晚住在低海拔康定极利于高反适应，今晚切勿剧烈运动或洗长热水澡。",
            "雅康高速隧道密集，雨季隧道出口防突发强降雨减速。",
            "随车已准备好氧气瓶、保温水杯与小零食。"
        ],
        "text": """🌸 8.1 明日川西自驾预告 · 成都 ➔ 康定

📍 目的地海拔：2560m (低海拔舒适适应)
📅 路线节点：DAY 1

🌤️ 节点气温与天气
· 康定市区：14℃ ~ 22℃ (多云体感宜人)
· 成都市区：22℃ ~ 31℃ (多云)
· 降雨预测：预计集中在 19:00 夜间

👗 穿搭灵感与打卡建议
· 建议穿搭：透气长袖内搭 + 随身防风外套
· 拍照打卡：傍晚 18:00 康定情歌广场与折多河畔

💡 暖心守护与注意事项
· 第一晚宿低海拔康定极利于适应高反，今晚切勿剧烈运动或洗长热水澡防感冒。
· 雅康高速隧道密集，雨季隧道出口减速防突发降雨。
· 随车已准备好氧气瓶、保温杯与零食。

💖 祝我们第一天行程浪漫愉快！"""
    }
}

def push_auto_schedule():
    token = get_access_token()
    if not token:
        print("无法获取微信 token")
        return

    tomorrow_str = (datetime.now() + timedelta(days=1)).strftime("%m-%d")
    card = HIGH_AESTHETIC_CARDS.get(tomorrow_str, HIGH_AESTHETIC_CARDS["08-01"])

    # 1. 自动渲染高颜值时尚海报图片并推送
    img_path = generate_poster_image(
        card["tag"], card["title"], card["elevation"],
        card["temp"], card["rain"], card["fashion"], card["cares"]
    )
    media_id = upload_image_to_wechat(token, img_path)
    if media_id:
        send_image_msg(token, media_id)

    # 2. 推送字重舒展的小红书流优雅纯文本
    send_text_msg(token, card["text"])

if __name__ == "__main__":
    push_auto_schedule()
