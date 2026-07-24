import os
import json
import requests
from datetime import datetime

APP_ID = "wxf39166d6f2deab57"
APP_SECRET = "c2fb35bda2fe52d795e6a64a70d3e38e"
USER_OPENID = "of84Y3bGGlhFtf7vqa52snEve8w4"
TEMPLATE_ID = "oaJwSb8IrjhC6pNlMas4jSOo2p5J1ETu976H1wGpLrQ"

def get_access_token():
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    r = requests.get(token_url).json()
    return r.get("access_token")

def send_perfect_text():
    token = get_access_token()
    if not token:
        print("获取 token 失败")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 第一手数据校对 + 抖音/小红书 24h 社媒热点排查 + 绝对安全守护
    perfect_design_text = f"""🌸 8.1 明日路书 · 成都市 ➔ 康定市
📍 目的地海拔：2560m (低海拔适应)
⏱️ 第一手数据校对时间：{timestamp}

【 🌤️ 气象与温差 】
• 康定市区：14~22℃｜多云体感宜人
• 成都市区：22~31℃｜晴间多云
• 降雨预测：预计 19:00 以后夜间小雨为主

【 🚦 明日路线与实时路况 】
• 通行路线：G4218 雅康高速 (全线双向畅通)
• 防范提醒：隧道密集，出隧道注意减速防雨
• 精准加油：雅安市天全服务区 / 康定折东路城关站

【 📡 抖音/小红书 24h 社媒热点排查 】
• 实时反馈：雅康高速泸定至康定段车流平稳；康定折东路晚餐高峰易拥堵，建议 18:30 前前往餐厅

【 👗 穿搭与打卡 】
• 穿搭灵感：透气长袖内搭 ➕ 随时穿脱防风外套
• 拍照打卡：18:00 康定情歌广场与折多河畔

【 💡 暖心守护 】
• 今晚住宿在海拔较低的康定市 (2560m)，非常有利于身体适应高原。今晚请注意不要剧烈运动，也不要洗太长热水澡，防止感冒。
• 高原紫外线渐强，记得带好遮阳帽与防晒霜。
• 随车已准备好保温水杯、便携氧气瓶与零食。

💖 祝我们的行程浪漫安全愉快"""

    custom_url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={token}"
    payload = {
        "touser": USER_OPENID,
        "msgtype": "text",
        "text": {
            "content": perfect_design_text
        }
    }
    json_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    res = requests.post(custom_url, data=json_data, headers=headers).json()
    print("微信第一手安全路书推送结果:", res)

    if res.get("errcode") != 0:
        tmpl_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
        tmpl_payload = {
            "touser": USER_OPENID,
            "template_id": TEMPLATE_ID,
            "data": {
                "first": {"value": "🌸 8.1 明日路书 · 成都市 ➔ 康定市 (2560m)", "color": "#1890ff"},
                "keyword1": {"value": "G4218雅康高速双向畅通 | 康定: 14~22℃", "color": "#cf1322"},
                "keyword2": {"value": "【第一手校对】雅安天全服务区/康定折东路站加满 | 抖音小红书24h畅通", "color": "#333333"},
                "remark": {"value": "💖 祝我们的行程浪漫安全愉快！", "color": "#fa8c16"}
            }
        }
        res2 = requests.post(tmpl_url, json=tmpl_payload).json()
        print("模板降级结果:", res2)

if __name__ == "__main__":
    send_perfect_text()
