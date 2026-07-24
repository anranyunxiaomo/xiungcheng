import os
import json
import requests

APP_ID = "wxf39166d6f2deab57"
APP_SECRET = "c2fb35bda2fe52d795e6a64a70d3e38e"
USER_OPENID = "of84Y3bGGlhFtf7vqa52snEve8w4"

DETAIL_URL = "https://anranyunxiaomo.github.io/xiungcheng/travel_plan_guide.html"

def get_access_token():
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    r = requests.get(token_url).json()
    return r.get("access_token")

def send_native_text():
    token = get_access_token()
    if not token:
        print("获取 token 失败")
        return

    text_content = f"""🏔️ 【川西 8.1–8.9 实时路况与气象播报】

⏱️ 播报时间：2026-07-24 09:27

📊 【今日 (7.24) vs 昨日 (7.23) 核心对比】
• 康定市：10~24℃ (多云有阵雨，气温维持)
• 折多山：12~21℃ (大雾伴小雨，建议走S434绕行)
• 理塘县：6~19℃ (多云转晴，较昨日转晴)
• 巴塘县：16~29℃ (河谷偏热，今晚必须加满油)
• G318国道：全线双向畅通，维持绿灯
• S569省道：08:00-12:00 封闭，窗口12:00-14:00

🛣️ 【重点路况与避坑警报】
1. 折多山大雾请开雾灯减速；
2. S569甲根坝施工，8.7去冷嘎措须卡准 12:00-14:00 窗口通过或绕行 G248 沙德段；
3. 格聂南线非铺装段水毁积水，四驱 SUV 满油通行，2026环保红线：严禁车驶离路基压草滩！

⛽ 【断油特警】
进入格聂南线前，必须在【中国石油巴塘县城加油站】加满油！腹地 250km 无正规站。

🔗 <a href="{DETAIL_URL}">点击直接打开全屏网页路书与地图</a>"""

    custom_url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={token}"
    payload = {
        "touser": USER_OPENID,
        "msgtype": "text",
        "text": {
            "content": text_content
        }
    }
    
    # 关键点：禁用 ensure_ascii，强制使用 utf-8 字节编码发送，彻底解决微信端 \uXXXX 乱码！
    json_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    
    res = requests.post(custom_url, data=json_data, headers=headers).json()
    print("微信原生无乱码文本推送结果:", res)

if __name__ == "__main__":
    send_native_text()
