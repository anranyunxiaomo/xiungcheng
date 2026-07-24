import os
import json
import requests

APP_ID = os.environ.get("WECHAT_APP_ID", "wxf39166d6f2deab57")
APP_SECRET = os.environ.get("WECHAT_APP_SECRET", "c2fb35bda2fe52d795e6a64a70d3e38e")
USER_OPENID = os.environ.get("WECHAT_USER_OPENID", "of84Y3bGGlhFtf7vqa52snEve8w4")

def get_access_token():
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    try:
        r = requests.get(token_url).json()
        return r.get("access_token")
    except Exception as e:
        print("获取 token 异常:", e)
        return None

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
    print("定时微信消息推送结果:", res)
    return res

def push_all_in_wechat():
    token = get_access_token()
    if not token:
        print("无法获取微信 token，放弃推送")
        return

    msg1 = """🏔️ 【川西 8.1–8.9 全景路书·微信直展版 (上)】

⏱️ 播报时间：2026-07-24 09:27

📊 【今日 (7.24) vs 昨日 (7.23) 核心比对】
• 康定市：10~24℃ (多云有阵雨，气温维持)
• 折多山：12~21℃ (大雾伴小雨，建议走S434绕行)
• 理塘县：6~19℃ (多云转晴，较昨日转晴)
• 巴塘县：16~29℃ (河谷偏热，今晚必须加满油)
• G318国道：全线双向畅通，维持绿灯
• S569省道：08:00-12:00 封闭，窗口12:00-14:00

⛽ 【沿线正规加油站分布清单】
1. 雅安天全服务区 / 中石油康定城关站 (折东路)
2. 中石油新都桥加油站 (G318国道旁镇中心)
3. 中石油雅江城关加油站 (河口镇G318段)
4. 中石油理塘城关站 / 理塘长青春站
5. 中石油巴塘县城加油站 (🚨进格聂前的最后正规站！必须彻底加满！)
6. 格聂南线腹地：❌无正规站，严禁空油深入！"""

    msg2 = """📅 【8.1 – 8.9 逐日精细行程卡片 (第1部分)】

🟢 DAY 1 (8.1) 成都 ➔ 康定 (海拔2560m)
• 气温：14~22℃ (多云转小雨)
• 降雨：19:00 以后集中
• 注意事项：第一晚切勿洗长热水澡防高反，雅康高速隧道出口防强降雨。

🟡 DAY 2 (8.2) 康定 ➔ 折多山 ➔ 鱼子西 ➔ 雅江 (海拔2600m)
• 气温：折多山5~12℃ / 雅江16~25℃
• 注意事项：早07:30出发翻折多山避堵；山顶大雾走S434绕新都桥；格底拉姆收约20元清洁费。

🟢 DAY 3 (8.3) 雅江 ➔ 理塘 ➔ 巴塘 (海拔2560m)
• 气温：理塘8~18℃ / 巴塘18~28℃
• 🚨断油特警：必须在【中国石油巴塘县城加油站】彻底加满油箱！

🔴 DAY 4 (8.4) 巴塘 ➔ 扎瓦拉 ➔ 夯达营地 ➔ 则巴村 (格聂南线)
• 气温：扎瓦拉2~8℃ (极寒) / 则巴村6~15℃
• 🚨高危警报：四驱高底盘SUV满油通行；扎瓦拉停留<20分钟；2026环保红线：严禁车驶离路基压草滩(违者重罚5万-20万)！"""

    msg3 = """📅 【8.1 – 8.9 逐日精细行程卡片 (第2部分)】

🟡 DAY 5 (8.5) 则巴村 ➔ 冷古寺 ➔ 铁匠山 ➔ 理塘/新都桥
• 气温：6~15℃ (湿度大)
• 注意事项：冷古寺徒步备防水鞋；格聂之眼严禁开车驶入草滩；出格聂抵理塘第一时间加满油。

🟢 DAY 6 (8.6) 理塘 ➔ 新都桥 (海拔3300m)
• 气温：理塘8~18℃ / 新都桥10~20℃
• 注意事项：赶路休整日，新都桥十里长廊散步摄影；防范G318坡脚零星落石。

🟡 DAY 7 (8.7) 新都桥 ➔ 冷嘎措 (海拔4500m) ➔ 新都桥
• 气温：冷嘎措山顶3~11℃ (极寒强风)
• 🚨修路管制：S569线K16-K54段08:00-12:00全封闭；方案1卡准12:00-14:00窗口通过；方案2走G248沙德绕行；带羽绒服保暖。

🟡 DAY 8 (8.8) 新都桥 ➔ 折多山 ➔ 康定 ➔ 成都
• 气温：折多山5~12℃ / 成都22~31℃
• 注意事项：建议早07:00前翻折多山避堵；堵车走S434绕行。

🟢 DAY 9 (8.9) 成都市区 ➔ 机场返程
• 气温：23~32℃ (多云小雨)
• 注意事项：还车前加满油，顺利返程！"""

    send_msg(token, msg1)
    send_msg(token, msg2)
    send_msg(token, msg3)

if __name__ == "__main__":
    push_all_in_wechat()
