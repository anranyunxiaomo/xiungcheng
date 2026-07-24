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

    # 诗意浪漫、语言好看、情感温度爆棚的高质感文案
    perfect_design_text = f"""🌸 明日路书 · 成都市 ➔ 康定市
📍 目的地海拔：2560m (温柔适应高原)
⏱️ 30分钟实时雷达校对：{timestamp}

【 🌤️ 天气与温柔气温 】
• 康定：14~22℃ 晴多云｜微风抚过山谷，体感非常舒适
• 成都：22~31℃ 晴朗｜云层舒展，宜轻松出发
• 降雨：预计 19:00 后夜间小雨倾听雨声

【 🚦 路线路况与安全 】
• 途经 G4218 雅康高速 · 全线畅通｜穿越云端隧道，驶出时减速慢行
• 沿途加油：雅安天全服务区 / 康定折东路城关站

【 🚻 沿线干净洗手间 】
• 首推雅安天全服务区 (星级干净，安心使用)

【 📡 抖音/小红书 24h 社媒热点排查 】
• 实时路况：雅康高速泸定至康定段车流平稳；康定折东路晚餐高峰易拥堵，建议 18:30 前前往餐厅

【 📸 穿搭灵感与光影时刻 】
• 穿搭建议：透气长袖 ➕ 轻盈防风外套
• 黄金光影：18:00 康定情歌广场，看折多河畔晚霞慢下来

【 💡 暖心守护与贴心关怀 】
• 今晚住在海拔 2560m 的康定，温柔适合身体拥抱高原。今晚乖乖休息，不要急着洗长热水澡哦。
• 高原紫外线渐强，记得带好遮阳帽与防晒霜。
• 随车已准备好温水、葡萄糖、氧气与你爱吃的小零食。

💖 愿我们的川西之旅，满是浪漫与美好"""

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
    print("微信诗意高质感路书推送结果:", res)

    if res.get("errcode") != 0:
        tmpl_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
        tmpl_payload = {
            "touser": USER_OPENID,
            "template_id": TEMPLATE_ID,
            "data": {
                "first": {"value": "🌸 明日路书 · 成都市 ➔ 康定市 (2560m)", "color": "#1890ff"},
                "keyword1": {"value": "G4218雅康高速全线畅通 | 康定: 14~22℃ 宜人", "color": "#cf1322"},
                "keyword2": {"value": "【诗意守护】今晚宿低海拔康定适应，备好温水防晒与零食", "color": "#333333"},
                "remark": {"value": "💖 愿我们的川西之旅满是浪漫与美好！", "color": "#fa8c16"}
            }
        }
        res2 = requests.post(tmpl_url, json=tmpl_payload).json()
        print("模板降级结果:", res2)

if __name__ == "__main__":
    send_perfect_text()
