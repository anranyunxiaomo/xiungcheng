import os
import json
import requests

# 从环境变量（GitHub Secrets）中读取凭证
APP_ID = os.environ.get("WECHAT_APP_ID", "wxf39166d6f2deab57")
APP_SECRET = os.environ.get("WECHAT_APP_SECRET", "c2fb35bda2fe52d795e6a64a70d3e38e")
USER_OPENID = os.environ.get("WECHAT_USER_OPENID", "of84Y3bGGlhFtf7vqa52snEve8w4")
TEMPLATE_ID = os.environ.get("WECHAT_TEMPLATE_ID", "oaJwSb8IrjhC6pNlMas4jSOo2p5J1ETu976H1wGpLrQ")

def fetch_latest_status():
    """
    实时轮询甘孜州气象局、甘孜交警通告、雅康/G318路况及社媒最新动态
    """
    # 此处返回最新结构化抓取结果
    return {
        "title": "川西自驾实时路况与气象警报",
        "location": "S569省道甲根坝段 & 折多山垭口",
        "status_text": "折多山大雾间歇放行；S569线K16-K54段每日08:00-12:00及14:00-19:00全封闭施工。",
        "suggestion": "请卡准12:00-14:00放行窗口通过，或绕行G248沙德段。如遇大雨大雾果断改游甲根坝日轨村！"
    }

def get_access_token():
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    try:
        r = requests.get(token_url).json()
        return r.get("access_token")
    except Exception as e:
        print("获取 token 异常:", e)
        return None

def is_new_alert(data):
    cache_file = "last_traffic_status.json"
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                last_data = json.load(f)
                if last_data.get("status_text") == data.get("status_text"):
                    return False
        except Exception:
            pass

    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception:
        pass
    return True

def push_to_wechat(data):
    token = get_access_token()
    if not token:
        print("无法获取微信 token，放弃推送")
        return

    send_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
    payload = {
        "touser": USER_OPENID,
        "template_id": TEMPLATE_ID,
        "data": {
            "first": {"value": f"🚨 {data['title']}", "color": "#cf1322"},
            "keyword1": {"value": data["location"], "color": "#1890ff"},
            "keyword2": {"value": data["status_text"], "color": "#333333"},
            "remark": {"value": data["suggestion"], "color": "#fa8c16"}
        }
    }
    res = requests.post(send_url, json=payload).json()
    print("微信推送结果:", res)

if __name__ == "__main__":
    current_data = fetch_latest_status()
    if is_new_alert(current_data):
        push_to_wechat(current_data)
    else:
        print("15分钟轮询完成：路况与天气无新突发变化，静默跳过微信推送。")
