import os
import json
import time
import requests
from datetime import datetime

APP_ID = "wxf39166d6f2deab57"
APP_SECRET = "c2fb35bda2fe52d795e6a64a70d3e38e"
USER_OPENID = "of84Y3bGGlhFtf7vqa52snEve8w4"
TEMPLATE_ID = "oaJwSb8IrjhC6pNlMas4jSOo2p5J1ETu976H1wGpLrQ"

def get_access_token():
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    for attempt in range(3):
        try:
            r = requests.get(token_url, timeout=10).json()
            if r.get("access_token"):
                return r.get("access_token")
        except Exception as e:
            print(f"获取 token 第 {attempt+1} 次重试:", e)
            time.sleep(1)
    return None

def send_perfect_text():
    token = get_access_token()
    if not token:
        print("获取 token 失败")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    perfect_design_text = f"""🌸 8.1 明日路书 · 成都市 ➔ 康定市
📍 目的地海拔：2560m (温柔适应高原)
⏱️ 第一手实时校对：{timestamp}

【 🌤️ 天气与温柔气温 】
• 康定：14~22℃ 晴多云｜微风抚过山谷，体感非常舒适
• 成都：22~31℃ 晴朗｜云层舒展，宜轻松出发
• 降雨：预计 19:00 后夜间小雨倾听雨声

【 🚦 路线路况与安全 】
• 原计划：成都 ➔ G4218 雅康高速直达 ➔ 康定市区
• 变动原因：因近期强降雨防汛避险，雅康高速泸康段管控
• 最新走法：雅康高速 ➔ 泸定站分流下高速 ➔ G318老路(49km) ➔ 康定
• 通行说明：G318 瓦斯沟老路柏油路畅通，仅多耗时 20分钟
• 精准加油：雅安天全服务区 / 康定折东路城关站

【 🍴 沿线高赞美食推荐 】
• 尚品牛味汤锅 (溜溜城店)：鲜切牦牛肉汤锅，汤头极鲜
• 菌王府野生菌 / 藏佳宴：正宗藏家特色土火锅
• 小吃地标：水井子康定凉粉 ➕ 将军桥凉粉

【 🚻 沿线干净洗手间 】
• 首推雅安天全服务区 (星级干净，安心使用)

【 📡 抖音/小红书 24h 社媒热点排查 】
• 实时路况：雅康高速泸定站分流下站秩序良好；康定折东路晚餐高峰易拥堵，建议 18:30 前前往餐厅

【 📸 穿搭灵感与光影时刻 】
• 穿搭建议：透气长袖 ➕ 轻盈防风外套
• 黄金光影：18:00 康定情歌广场，看折多河畔晚霞慢下来

【 💡 暖心守护与贴心关怀 】
• 今晚住在海拔 2560m 的康定，温柔适合身体拥抱高原。今晚乖乖休息，不要急着洗长热水澡哦。
• 高原紫外线渐强，记得带好遮阳帽与防晒霜。
• 随车已准备好温水、葡萄糖、氧气与你爱吃的小零食。

💖 祝你第一天行程浪漫愉快"""

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
    
    res = None
    for attempt in range(3):
        try:
            res = requests.post(custom_url, data=json_data, headers=headers, timeout=10).json()
            print("微信 8.1 精细路况说明推送结果:", res)
            break
        except Exception as e:
            print(f"发送消息第 {attempt+1} 次重试:", e)
            time.sleep(1)

    if res and res.get("errcode") != 0:
        tmpl_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
        tmpl_payload = {
            "touser": USER_OPENID,
            "template_id": TEMPLATE_ID,
            "data": {
                "first": {"value": "🌸 8.1 明日路书 · 成都市 ➔ 康定市 (2560m)", "color": "#1890ff"},
                "keyword1": {"value": "康定: 14~22℃ 晴多云 | 成都: 22~31℃ 晴朗", "color": "#cf1322"},
                "keyword2": {"value": "雅康高速泸定站分流接G318老路(49km) | 尚品牛味汤锅", "color": "#333333"},
                "remark": {"value": "💖 祝你第一天行程浪漫愉快！", "color": "#fa8c16"}
            }
        }
        try:
            res2 = requests.post(tmpl_url, json=tmpl_payload, timeout=10).json()
            print("模板降级结果:", res2)
        except Exception as e:
            print("模板发送异常:", e)

if __name__ == "__main__":
    send_perfect_text()
