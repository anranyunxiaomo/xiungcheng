import os
import json
import requests

APP_ID = os.environ.get("WECHAT_APP_ID", "wxf39166d6f2deab57")
APP_SECRET = os.environ.get("WECHAT_APP_SECRET", "c2fb35bda2fe52d795e6a64a70d3e38e")
USER_OPENID = os.environ.get("WECHAT_USER_OPENID", "of84Y3bGGlhFtf7vqa52snEve8w4")
TEMPLATE_ID = os.environ.get("WECHAT_TEMPLATE_ID", "oaJwSb8IrjhC6pNlMas4jSOo2p5J1ETu976H1wGpLrQ")

DETAIL_URL = "https://anranyunxiaomo.github.io/xiungcheng/travel_plan_guide.html"
PIC_URL = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1200&auto=format&fit=crop"

def fetch_latest_status_with_compare():
    return {
        "title": "🏔️ 川西 8.1–8.9 路线 7.24 实时路况与气象全景简报",
        "location": "折多山 / S569甲根坝 / 理塘巴塘 / 格聂南线",
        "status_text": "【今日实时排查与差分比对】\n• 🛑 折多山垭口：大雾伴小雨，视线较差，推荐走 S434 省道绕行；\n• 🚧 S569 甲根坝段：K16-K54 段维持 08:00-12:00 及 14:00-19:00 全封闭施工，放行窗口 12:00-14:00；\n• ☀️ 理塘与巴塘：理塘多云转晴，夜间清冷；巴塘河谷偏热，今晚必须加满油；\n• 🔴 格聂南线：非铺装路段水毁积水较多，四驱高底盘 SUV 满油通行，绝对严禁车辆驶离路基！",
        "suggestion": "👉 点击卡片直接查看 9 天卡片、加油站清单与每日对比！"
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

    # 1. 优先使用大图文卡片 (News Card)
    custom_url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={token}"
    news_payload = {
        "touser": USER_OPENID,
        "msgtype": "news",
        "news": {
            "articles": [
                {
                    "title": data["title"],
                    "description": data["status_text"],
                    "url": DETAIL_URL,
                    "picurl": PIC_URL
                }
            ]
        }
    }
    res = requests.post(custom_url, json=news_payload).json()
    print("微信图文大卡片 (News Card) 推送结果:", res)

    # 2. 若无 48h 交互授权，降级为模板消息
    if res.get("errcode") != 0:
        send_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
        payload = {
            "touser": USER_OPENID,
            "template_id": TEMPLATE_ID,
            "url": DETAIL_URL,
            "data": {
                "first": {"value": f"📊 {data['title']}", "color": "#1890ff"},
                "keyword1": {"value": data["location"], "color": "#cf1322"},
                "keyword2": {"value": data["status_text"], "color": "#333333"},
                "remark": {"value": data["suggestion"], "color": "#fa8c16"}
            }
        }
        res2 = requests.post(send_url, json=payload).json()
        print("微信模板消息降级推送结果:", res2)

if __name__ == "__main__":
    current_data = fetch_latest_status_with_compare()
    if is_new_alert(current_data):
        push_to_wechat(current_data)
    else:
        print("轮询完成：数据比对无新突发差异，静默跳过微信推送。")
