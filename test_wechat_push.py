import requests

APP_ID = "wxf39166d6f2deab57"
APP_SECRET = "c2fb35bda2fe52d795e6a64a70d3e38e"
USER_OPENID = "of84Y3bGGlhFtf7vqa52snEve8w4"
TEMPLATE_ID = "oaJwSb8IrjhC6pNlMas4jSOo2p5J1ETu976H1wGpLrQ"

def send_test():
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
            "first": {"value": "🏔️ 川西 8.1-8.9 秘境自驾路书服务已连接", "color": "#1890ff"},
            "keyword1": {"value": "S569省道甲根坝段 & 折多山垭口", "color": "#cf1322"},
            "keyword2": {"value": "连线成功！已接入甘孜气象局、交警通告及雅康/G318路况实时监控！", "color": "#333333"},
            "remark": {"value": "预祝您与她的川西秘境之旅安全顺利完美！突发路况将第一时间推送到此微信。", "color": "#fa8c16"}
        }
    }
    res = requests.post(send_url, json=payload).json()
    print("微信推送结果:", res)

if __name__ == "__main__":
    send_test()
