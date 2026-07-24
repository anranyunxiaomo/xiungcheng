import os
import json
import subprocess
import requests

APP_ID = "wxf39166d6f2deab57"
APP_SECRET = "c2fb35bda2fe52d795e6a64a70d3e38e"
USER_OPENID = "of84Y3bGGlhFtf7vqa52snEve8w4"

cwd = "/Users/anranyunxiaomo/Desktop/project/xiungcheng"
html_path = os.path.join(cwd, "daily_poster_demo.html")
img_path = os.path.join(cwd, "daily_poster_demo.png")

def get_access_token():
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    r = requests.get(token_url).json()
    return r.get("access_token")

def upload_image_to_wechat(token, file_path):
    upload_url = f"https://api.weixin.qq.com/cgi-bin/media/upload?access_token={token}&type=image"
    with open(file_path, "rb") as f:
        files = {"media": f}
        res = requests.post(upload_url, files=files).json()
    print("微信素材上传结果:", res)
    return res.get("media_id")

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
    res = requests.post(custom_url, data=json_data, headers=headers).json()
    print("微信海报图片消息推送结果:", res)
    return res

def send_elegant_text_msg(token, text_content):
    custom_url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={token}"
    payload = {
        "touser": USER_OPENID,
        "msgtype": "text",
        "text": {
            "content": text_content
        }
    }
    json_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    res = requests.post(custom_url, data=json_data, headers=headers).json()
    print("微信优雅文本推送结果:", res)
    return res

def run():
    token = get_access_token()
    if not token:
        print("获取 token 失败")
        return

    # 1. 生成并推送美感炸裂的时尚卡片海报图片
    media_id = upload_image_to_wechat(token, img_path)
    if media_id:
        send_image_msg(token, media_id)

    # 2. 搭配一条去掉了难看下划线、字重舒展的小红书流优雅纯文本
    elegant_text = """🌸 8.1 明日川西自驾预告 · 成都 ➔ 康定

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

    send_elegant_text_msg(token, elegant_text)

if __name__ == "__main__":
    run()
