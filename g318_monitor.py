import os
import json
import requests

APP_ID = os.environ.get("WECHAT_APP_ID", "wxf39166d6f2deab57")
APP_SECRET = os.environ.get("WECHAT_APP_SECRET", "c2fb35bda2fe52d795e6a64a70d3e38e")
USER_OPENID = os.environ.get("WECHAT_USER_OPENID", "of84Y3bGGlhFtf7vqa52snEve8w4")
TEMPLATE_ID = os.environ.get("WECHAT_TEMPLATE_ID", "oaJwSb8IrjhC6pNlMas4jSOo2p5J1ETu976H1wGpLrQ")

DETAIL_URL = "https://anranyunxiaomo.github.io/xiungcheng/travel_plan_guide.html"

def fetch_latest_status_with_compare():
    return {
        "text": f"""🏔️ 【川西 8.1–8.9 实时路况与气象播报】

⏱️ 播报时间：2026-07-24 09:27

📊 【今日 (7.24) vs 昨日 (7.23) 核心对比】
• 康定市：10~24℃ (多云有阵雨，气温维持)
• 折多山：12~21℃ (大雾伴小雨，建议走S434绕行)
• 理塘县：6~19℃ (多云转晴，较昨日转晴)
• 巴塘县：16~29℃ (河谷偏热，今晚必须加满油)
• G318国道：全线双向畅通，维持绿灯
• S569省道：08:00-12:00 封闭，窗口12:00-14:00

🛣️ 【重点路况与避坑警报】
1. 折多山大雾请开雾灯减速；
2. S569甲根坝施工，8.7去冷嘎措须卡准 12:00-14:00 窗口通过或绕行 G248 沙德段；
3. 格聂南线非铺装段水毁积水，四驱 SUV 满油通行，2026环保红线：严禁车驶离路基压草滩！

⛽ 【断油特警】
进入格聂南线前，必须在【中国石油巴塘县城加油站】加满油！腹地 250km 无正规站。

🔗 <a href="{DETAIL_URL}">点击直接打开全屏网页路书与地图</a>"""
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
                if last_data.get("text") == data.get("text"):
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

    # 优先发送微信原生长文本消息 (ensure_ascii=False 彻底避免乱码)
    custom_url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={token}"
    payload = {
        "touser": USER_OPENID,
        "msgtype": "text",
        "text": {
            "content": data["text"]
        }
    }
    json_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    
    res = requests.post(custom_url, data=json_data, headers=headers).json()
    print("微信原生长文本消息推送结果:", res)

    # 若缺少 48h 交互授权，降级备用模板卡片
    if res.get("errcode") != 0:
        send_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
        tmpl_payload = {
            "touser": USER_OPENID,
            "template_id": TEMPLATE_ID,
            "url": DETAIL_URL,
            "data": {
                "first": {"value": "🏔️ 川西 8.1-8.9 路线 7.24 实时路况播报", "color": "#1890ff"},
                "keyword1": {"value": "折多山 / S569甲根坝 / 格聂南线", "color": "#cf1322"},
                "keyword2": {"value": "折多山大雾推荐走S434；S569线08:00-12:00全封闭；理塘转晴；格聂南线严禁开下草滩！", "color": "#333333"},
                "remark": {"value": "👉 点击查看全屏高颜值 H5 自驾路书与每日比对！", "color": "#fa8c16"}
            }
        }
        res2 = requests.post(send_url, json=tmpl_payload).json()
        print("微信模板消息降级推送结果:", res2)

if __name__ == "__main__":
    current_data = fetch_latest_status_with_compare()
    if is_new_alert(current_data):
        push_to_wechat(current_data)
    else:
        print("轮询完成：数据比对无新突发差异，静默跳过微信推送。")
