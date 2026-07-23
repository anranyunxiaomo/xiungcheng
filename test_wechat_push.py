import requests

APP_ID = "wxf39166d6f2deab57"
APP_SECRET = "c2fb35bda2fe52d795e6a64a70d3e38e"
USER_OPENID = "of84Y3bGGlhFtf7vqa52snEve8w4"
TEMPLATE_ID = "oaJwSb8IrjhC6pNlMas4jSOo2p5J1ETu976H1wGpLrQ"

def send_real_test():
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    r = requests.get(token_url).json()
    token = r.get("access_token")
    if not token:
        print("获取 token 失败:", r)
        return
    
    send_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
    payload = {
        "touser": USER_OPENID,
        "template_id": TEMPLATE_ID,
        "data": {
            "first": {"value": "🏔️ 川西 8.1-8.9 路线实时路况与天气播报", "color": "#1890ff"},
            "keyword1": {"value": "S569省道甲根坝段 & 折多山垭口", "color": "#cf1322"},
            "keyword2": {"value": "折多山垭口目前多云伴有大雾；S569线K16-K54段施工，08:00-12:00及14:00-19:00全封闭管制！", "color": "#333333"},
            "remark": {"value": "💡 贴心指南：8月7日去冷嘎措请卡准 12:00-14:00 窗口通过，或绕行 G248 沙德段。8月3日巴塘请务必加满油！", "color": "#fa8c16"}
        }
    }
    res = requests.post(send_url, json=payload).json()
    print("微信推送结果:", res)

if __name__ == "__main__":
    send_real_test()
