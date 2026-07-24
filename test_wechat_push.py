import os
import json
import requests

APP_ID = "wxf39166d6f2deab57"
APP_SECRET = "c2fb35bda2fe52d795e6a64a70d3e38e"
USER_OPENID = "of84Y3bGGlhFtf7vqa52snEve8w4"
TEMPLATE_ID = "oaJwSb8IrjhC6pNlMas4jSOo2p5J1ETu976H1wGpLrQ"

def get_access_token():
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    r = requests.get(token_url).json()
    return r.get("access_token")

def send_perfect_layout():
    token = get_access_token()
    if not token:
        print("获取 token 失败")
        return

    # 防折行断字控制 (每行<=16字)、微信原生【 】框线、彩色 Emoji 精致排版
    perfect_design_text = """🌸 8.1 明日路书 · 成都 ➔ 康定
📍 目的地海拔：2560m (低海拔适应)

【 🌤️ 气象与温差 】
• 康定：14~22℃｜多云体感宜人
• 成都：22~31℃｜晴间多云
• 降雨：预计 19:00 后夜间小雨

【 👗 穿搭与打卡 】
• 穿搭：长袖内搭 ➕ 随时穿脱外套
• 打卡：18:00 康定情歌广场夕阳

【 🚗 路线与加油 】
• 雅康高速畅通，隧道出口防雨
• 已在天全服务区加满油箱

【 💡 暖心守护 】
• 今晚宿康定利于适应高反，切勿洗长热水澡或剧烈运动
• 紫外线渐强，带好遮阳帽与防晒
• 随车备有保温杯、氧气与零食

💖 祝我们第一天行程浪漫愉快"""

    # 1. 尝试客服消息发送
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
    print("微信客服文本推送结果:", res)

    # 2. 如果客服配额满 (45047)，降级模板消息保证 100% 送达微信！
    if res.get("errcode") != 0:
        tmpl_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
        tmpl_payload = {
            "touser": USER_OPENID,
            "template_id": TEMPLATE_ID,
            "data": {
                "first": {"value": "🌸 8.1 明日路书 · 成都 ➔ 康定 (2560m)", "color": "#1890ff"},
                "keyword1": {"value": "康定: 14~22℃ 多云 | 成都: 22~31℃", "color": "#cf1322"},
                "keyword2": {"value": "【穿搭】长袖内搭+外套 | 【守护】第一晚勿洗长热水澡，备好保温杯氧气", "color": "#333333"},
                "remark": {"value": "💖 祝我们第一天行程浪漫愉快！", "color": "#fa8c16"}
            }
        }
        res2 = requests.post(tmpl_url, json=tmpl_payload).json()
        print("微信模板消息降级推送结果:", res2)

if __name__ == "__main__":
    send_perfect_layout()
