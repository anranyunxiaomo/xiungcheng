import os
import requests

APP_ID = "wxf39166d6f2deab57"
APP_SECRET = "c2fb35bda2fe52d795e6a64a70d3e38e"
USER_OPENID = "of84Y3bGGlhFtf7vqa52snEve8w4"
TEMPLATE_ID = "oaJwSb8IrjhC6pNlMas4jSOo2p5J1ETu976H1wGpLrQ"

# 在线全景路书网页与高清封面图
DETAIL_URL = "https://anranyunxiaomo.github.io/xiungcheng/travel_plan_guide.html"
PIC_URL = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1200&auto=format&fit=crop"

def get_access_token():
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    r = requests.get(token_url).json()
    return r.get("access_token")

def send_news_card():
    token = get_access_token()
    if not token:
        print("获取 token 失败")
        return

    # 1. 尝试使用微信客服接口推送“大图文消息卡片 (News Card)”
    custom_url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={token}"
    news_payload = {
        "touser": USER_OPENID,
        "msgtype": "news",
        "news": {
            "articles": [
                {
                    "title": "🏔️ 川西 8.1–8.9 路线 7.24 实时路况与气象全景简报",
                    "description": "【今日实时排查与差分比对】\n• 🛑 折多山垭口：大雾伴小雨，视线较差，推荐走 S434 省道绕行；\n• 🚧 S569 甲根坝段：K16-K54 段维持 08:00-12:00 及 14:00-19:00 全封闭施工，放行窗口 12:00-14:00；\n• ☀️ 理塘与巴塘：理塘多云转晴，夜间清冷；巴塘河谷偏热，今晚必须加满油；\n• 🔴 格聂南线：非铺装路段水毁积水较多，四驱高底盘 SUV 满油通行，绝对严禁车辆驶离路基！\n\n点击直接查看 9 天卡片、加油站清单与每日对比！",
                    "url": DETAIL_URL,
                    "picurl": PIC_URL
                }
            ]
        }
    }
    
    res = requests.post(custom_url, json=news_payload).json()
    print("微信图文大卡片 (News Card) 推送结果:", res)
    
    # 如果客服图文接口因 48h 交互限制未成功，自动降级备用模板卡片
    if res.get("errcode") != 0:
        print("转为模板消息卡片推送...")
        template_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
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
        res2 = requests.post(template_url, json=tmpl_payload).json()
        print("模板消息推送结果:", res2)

if __name__ == "__main__":
    send_news_card()
