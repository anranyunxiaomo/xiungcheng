import os
import json
import time
import requests

APP_ID = "wxf39166d6f2deab57"
APP_SECRET = "c2fb35bda2fe52d795e6a64a70d3e38e"
USER_OPENID = "of84Y3bGGlhFtf7vqa52snEve8w4"

def get_access_token():
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    r = requests.get(token_url).json()
    return r.get("access_token")

def send_msg(token, content):
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
    res = requests.post(custom_url, data=json_data, headers=headers).json()
    print("推送结果:", res)
    return res

def send_romantic_demo():
    token = get_access_token()
    if not token:
        print("获取 token 失败")
        return

    # 专门为女生定制的【提前一天专属暖心路书卡片】范例 (7.31 晚推送 8.1 示例)
    msg_demo = """🌸 【8.1 明日川西自驾预告·给她的专属路书】
━━━━━━━━━━━━━━━━━━━━
✨ 8月1日 (DAY 1) 成都 ➔ 康定
📍 目的地海拔：2560m (低海拔舒适适应)

🌤️ 【天气与气温】
• 成都市区：22 ~ 31℃ (晴间多云)
• 康定市区：14 ~ 22℃ (多云伴微风，体感舒适)
🌧️ 降雨时段：预计集中在夜间 19:00 以后

👗 【穿搭与打卡建议】
• 穿搭建议：透气长袖内搭 + 随身防风外套
• 拍照打卡：傍晚 18:00 康定情歌广场与折多河畔

⛽ 【路线与加油】
• G4218 雅康高速全线畅通，隧道出口注意减速；
• 会在天全服务区或康定市区将油箱彻底加满。

💡 【贴心关怀与注意事项】
1. 第一晚住在低海拔的康定 (2560m) 特别有利于适应高原，今晚不要洗长热水澡或剧烈运动，预防感冒及高反；
2. 高原紫外线渐强，记得带好遮阳帽、墨镜与防晒霜；
3. 随车已准备好便携氧气瓶、保温水杯与高热量零食，安心出发！

💖 祝我们的川西秘境之旅第一天浪漫愉快！"""

    send_msg(token, msg_demo)

if __name__ == "__main__":
    send_romantic_demo()
