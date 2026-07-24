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
            "first": {"value": "🏔️ 川西 8.1-8.9 路线 7.24 实时路况与天气播报", "color": "#1890ff"},
            "keyword1": {"value": "折多山 / S569甲根坝 / G318川藏线", "color": "#cf1322"},
            "keyword2": {"value": "【7.24最新】G318全线双向畅通；折多山阴天局部有雾；S569线K16-K54段维持08:00-12:00全封闭施工。", "color": "#333333"},
            "remark": {"value": "💡 应急提示：理塘转晴偏冷；去冷嘎措请卡准 12:00-14:00 窗口通行或绕行 G248 沙德段。祝行程平安！", "color": "#fa8c16"}
        }
    }
    res = requests.post(send_url, json=payload).json()
    print("微信推送结果:", res)

if __name__ == "__main__":
    send_real_test()
