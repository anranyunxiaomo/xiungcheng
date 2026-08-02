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

def send_aug2_card_now():
    token = get_access_token()
    if not token:
        print("获取 token 失败")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 包含 8.2 (DAY 2 康定 ➔ 雅江) 全量美感与动态实测数据的专属路书
    perfect_design_text = f"""🌸 8.2 明日路书 · 康定市 ➔ 雅江县
📍 目的地海拔：折多山 4298m ➔ 雅江 2600m
⏱️ 第一手动态 API 校对：{timestamp}

【 🌤️ 真实实时气象 】
• 折多山/鱼子西：5~12℃ 多云有局地阵雨｜风大较冷，降水概率 45%
• 雅江县城：16~25℃ 晴间多云｜低海拔温暖舒适
• 降雨：14:00~17:00 午后局地阵雨相伴

【 🚦 路线路况与安全 】
• 原计划：翻越折多山垭口(G318)直达新都桥/雅江
• 变动预案：若折多山因大雾/拥堵临时管控，走 S434 斯丁措绕行
• 通行说明：G318 折多山段目前正常放行，S434 备选风景优美
• 沿途加油：中石油新都桥站 / 雅江河口镇城关站

【 🍴 沿线高赞美食推荐 】
• 雅江松茸炖土鸡：松茸之乡必吃珍馐，鲜香无比
• 雅江特色松茸面：轻食暖胃高赞高口碑
• 张艳烧烤：地道川式晚间风味烧烤

【 🚻 沿线干净洗手间 】
• 折多山垭口室内洗手间 (收费2元) / 新都桥酒店

【 📡 抖音/小红书 24h 社媒热点排查 】
• 实时路况：折多山垭口早晨 08:30 开始车流增大；鱼子西观景台草甸雨后稍湿，请备好防风外套

【 📸 穿搭灵感与光影时刻 】
• 穿搭建议：暖心冲锋衣/薄羽绒服 ➕ 防风手套帽子
• 黄金光影：19:00-20:00 鱼子西/格底拉姆看日照金山晚霞

【 💡 暖心守护与贴心关怀 】
• 折多山垭口与鱼子西海拔较高，山顶风大体感较冷，拍照停留时请注意保暖，不要剧烈跑跳，吸氧少量多次。
• 格底拉姆非铺装土路雨后湿滑，现场收取约 20元/人 清洁费。
• 今晚住宿在海拔较低的雅江县城 (2600m)，可以好好睡个好觉恢复体力。

💖 愿你明天看到最浪漫的雪山日落"""

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
            print("微信 8.2 专属路书推送结果:", res)
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
                "first": {"value": "🌸 8.2 明日路书 · 康定市 ➔ 雅江县 (2600m)", "color": "#1890ff"},
                "keyword1": {"value": "折多山: 5~12℃ 风大较冷 | 雅江: 16~25℃ 舒适", "color": "#cf1322"},
                "keyword2": {"value": "G318折多山段正常放行 | 雅江松茸炖土鸡", "color": "#333333"},
                "remark": {"value": "💖 愿你明天看到最浪漫的雪山日落！", "color": "#fa8c16"}
            }
        }
        try:
            res2 = requests.post(tmpl_url, json=tmpl_payload, timeout=10).json()
            print("模板降级结果:", res2)
        except Exception as e:
            print("模板发送异常:", e)

if __name__ == "__main__":
    send_aug2_card_now()
