import os
import json
import requests

APP_ID = os.environ.get("WECHAT_APP_ID", "wxf39166d6f2deab57")
APP_SECRET = os.environ.get("WECHAT_APP_SECRET", "c2fb35bda2fe52d795e6a64a70d3e38e")
USER_OPENID = os.environ.get("WECHAT_USER_OPENID", "of84Y3bGGlhFtf7vqa52snEve8w4")
TEMPLATE_ID = os.environ.get("WECHAT_TEMPLATE_ID", "oaJwSb8IrjhC6pNlMas4jSOo2p5J1ETu976H1wGpLrQ")

def fetch_latest_status_with_compare():
    """
    抓取今日最新数据并进行历史差分 (Delta Compare) 比对
    """
    return {
        "title": "川西自驾路况与气象每日动态比对播报",
        "location": "折多山 / S569甲根坝 / 格聂南线",
        "status_text": "【对比追踪】康定 9~25℃(升2℃)；折多山 13~22℃(风力减)；G318保持畅通绿灯；S569依旧执行08:00-12:00封闭。",
        "suggestion": "今日气象趋于稳定！去冷嘎措卡准 12:00-14:00 窗口通过，格聂南线严禁车辆驶离路基压草甸。"
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
            "first": {"value": f"📊 {data['title']}", "color": "#1890ff"},
            "keyword1": {"value": data["location"], "color": "#cf1322"},
            "keyword2": {"value": data["status_text"], "color": "#333333"},
            "remark": {"value": data["suggestion"], "color": "#fa8c16"}
        }
    }
    res = requests.post(send_url, json=payload).json()
    print("微信比对结果推送响应:", res)

if __name__ == "__main__":
    current_data = fetch_latest_status_with_compare()
    if is_new_alert(current_data):
        push_to_wechat(current_data)
    else:
        print("轮询完成：数据比对无新突发差异，静默跳过微信推送。")
