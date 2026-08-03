import os
import json
import time
import requests
from datetime import datetime

APP_ID = "wxf39166d6f2deab57"
APP_SECRET = "c2fb35bda2fe52d795e6a64a70d3e38e"
USER_OPENID = "of84Y3bGGlhFtf7vqa52snEve8w4"
TEMPLATE_ID = "oaJwSb8IrjhC6pNlMas4jSOo2p5J1ETu976H1wGpLrQ"

def get_access_token():
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    for attempt in range(3):
        try:
            r = requests.get(token_url, timeout=10).json()
            if r.get("access_token"):
                return r.get("access_token")
        except Exception as e:
            print(f"获取 token 第 {attempt+1} 次重试:", e)
            time.sleep(1)
    return None

def send_perfect_aug4_card():
    token = get_access_token()
    if not token:
        print("获取 token 失败")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    perfect_design_text = f"""🌸 明日路书 · 格聂南线越野腹地
📍 地标海拔：扎瓦拉 5022m ➔ 则巴村 3900m
⏱️ 第一手动态 API 校对：{timestamp}

【 🌤️ 真实实时气象 】
• 格聂南线：14~21℃ 阵雨｜雨水润泽山谷，体感凉爽宜人 (降水概率 55%)

【 🚦 真实实时路况 】
• 原计划：穿越格聂南线越野腹地至则巴村
• 变动预案：若巴塘早晨预报大暴雨/泥石流，果断改走 G318 到理塘
• 通行说明：非铺装碎石水毁段，炮弹坑雨后积水较深
• 🚨 环保红线：严禁车辆开下路基压草滩 (重罚5万-20万)

【 🍴 沿线高赞美食推荐 】
• 则巴村民宿藏家手抓牦牛肉 ➕ 藏式暖心土火锅
• 随车特备：高热量巧克力、坚果与热腾腾的红茶

【 🚻 沿线干净洗手间 】
• 腹地无公共洗手间，在巴塘出发前及民宿解决

【 📡 抖音/小红书 24h 社媒热点排查 】
• 实时路况：夯达营地雨后炮弹坑有积水，建议慢速通过；格聂之眼执法人员巡查严格，严禁压草滩

【 📸 穿搭灵感与光影时刻 】
• 穿搭建议：最厚防风羽绒服 ➕ 贴身保暖内衣 ➕ 针织帽手套 (全线最冷日)
• 黄金光影：12:00 扎瓦拉垭口雪山全景与夯达营地牧场

【 💡 暖心守护与贴心关怀 】
• 扎瓦拉垭口海拔 5022 米，气温极低，拍照停留请不要超过 20 分钟防止高反，布洛芬放在易拿处。
• 特别注意：2026 年环保执法非常严格，严禁将车辆驶离路基开入草滩，违者会被重罚。
• 越野腹地部分区域没有信号，已提前准备好离线地图与保温水杯。

💖 深入格聂秘境，愿你拥抱最纯粹的雪山草原 (🚨极寒保暖预警)"""

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
    
    res = None
    for attempt in range(3):
        try:
            res = requests.post(custom_url, data=json_data, headers=headers, timeout=10).json()
            print("微信 8.4 独家专属精细路书推送结果:", res)
            break
        except Exception as e:
            print(f"发送消息第 {attempt+1} 次重试:", e)
            time.sleep(1)

    if res and res.get("errcode") != 0:
        tmpl_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
        tmpl_payload = {
            "touser": USER_OPENID,
            "template_id": TEMPLATE_ID,
            "data": {
                "first": {"value": "🌸 明日路书 · 格聂南线越野腹地 (5022m)", "color": "#1890ff"},
                "keyword1": {"value": "扎瓦拉垭口(5022m)仅2~8℃ 极寒 | 穿最厚羽绒服", "color": "#cf1322"},
                "keyword2": {"value": "严禁车辆驶离路基压草滩 | 夯达营地炮弹坑慢行", "color": "#333333"},
                "remark": {"value": "💖 深入格聂秘境，愿你拥抱最纯粹的雪山草原！", "color": "#fa8c16"}
            }
        }
        try:
            res2 = requests.post(tmpl_url, json=tmpl_payload, timeout=10).json()
            print("模板降级结果:", res2)
        except Exception as e:
            print("模板发送异常:", e)

if __name__ == "__main__":
    send_perfect_aug4_card()
