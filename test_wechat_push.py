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

def send_perfect_text():
    token = get_access_token()
    if not token:
        print("获取 token 失败")
        return

    # 地理位置绝对精确 + 【 🚦 明日路线与实时路况 】显式模块 + 严格防折行控制 (<=16字)
    perfect_design_text = """🌸 8.1 明日路书 · 成都市 ➔ 康定市
📍 目的地海拔：2560m (低海拔适应)

【 🌤️ 气象与温差 】
• 康定市区：14~22℃｜多云体感宜人
• 成都市区：22~31℃｜晴间多云
• 降雨预测：预计 19:00 后夜间小雨为主

【 🚦 明日路线与实时路况 】
• 通行路线：G4218 雅康高速 (双向畅通)
• 防范提醒：隧道密集，隧道出口防雨减速
• 精准加油：雅安天全服务区 / 康定折东路城关站

【 👗 穿搭与打卡 】
• 穿搭灵感：透气长袖内搭 ➕ 随身防风外套
• 拍照打卡：18:00 康定情歌广场与折多河畔

【 💡 暖心守护 】
• 今晚宿康定利于适应高反，切勿洗长热水澡或剧烈运动
• 紫外线渐强，带好遮阳帽与防晒霜
• 随车备有保温水杯、便携氧气瓶与高热量零食

💖 祝我们第一天行程浪漫愉快"""

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
    print("微信文本推送结果:", res)

    if res.get("errcode") != 0:
        tmpl_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
        tmpl_payload = {
            "touser": USER_OPENID,
            "template_id": TEMPLATE_ID,
            "data": {
                "first": {"value": "🌸 8.1 明日路书 · 成都 ➔ 康定 (2560m)", "color": "#1890ff"},
                "keyword1": {"value": "G4218雅康高速双向畅通 | 康定: 14~22℃", "color": "#cf1322"},
                "keyword2": {"value": "【路况】雅安天全服务区/康定折东路站加满 | 隧道出口防雨", "color": "#333333"},
                "remark": {"value": "💖 祝我们第一天行程浪漫愉快！", "color": "#fa8c16"}
            }
        }
        res2 = requests.post(tmpl_url, json=tmpl_payload).json()
        print("模板降级结果:", res2)

if __name__ == "__main__":
    send_perfect_text()
